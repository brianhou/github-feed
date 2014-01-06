import github
import sys

g = github.Github()

def not_found(default):
    def defaulted(fn):
        def protected(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except github.GithubException as e:
                print >> sys.stderr, e
                return default()
        return protected
    return defaulted

@not_found(lambda: None)
def get_user(username):
    """Returns a User object or None for an invalid username."""
    return g.get_user(username)

@not_found(list)
def get_repos(user):
    """Returns a list of USER's repos."""
    return list(user.get_repos())

@not_found(list)
def get_repo_commits(user, repo):
    """Returns a list of the last ten commits by USER in REPO."""
    commits = []
    for commit in repo.get_commits():
        if commit.author == user:
            commits.append((commit, repo.name))
        if len(commits) >= 10: # rate-limiting!
            break
    return commits

def get_commits(user):
    """Returns a list of recent commits by USER."""
    all_commits = []
    for repo in get_repos(user):
        all_commits.extend(get_repo_commits(user, repo))
    return all_commits

def recent_commits(username, n=10):
    """Returns a list of recent commits by USERNAME. Each commit is represented
    as a Commit object."""
    user = get_user(username)
    if user:
        user_commits = get_commits(user)
        user_commits.sort(key=lambda c: c[0].commit.author.date, reverse=True)
        return [Commit(*c) for c in user_commits[:n]]

class Commit(object):
    """Hold rendering information."""
    def __init__(self, commit_object, repo_name):
        self.message = commit_object.commit.message
        self.committer = commit_object.committer.name
        self.url = commit_object.commit.html_url
        self.repo_name = repo_name
        self.date = commit_object.commit.committer.date
