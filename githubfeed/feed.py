import pygithub3
import requests

gh = pygithub3.Github()

def not_found(default=None):
    def defaulted(fn):
        def protected(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except pygithub3.exceptions.NotFound:
                return default
            except requests.exceptions.HTTPError:
                print 'Remaining requests: %s' % gh.remaining_requests
                exit(1)
        return protected
    return defaulted

@not_found(())
def get_repos(username):
    return tuple(gh.repos.list(username).iterator())

@not_found(())
def get_commits(username): # oops rate limiting
    all_commits = []
    for repo in get_repos(username):
        print repo.name
        repo_commits = gh.repos.commits.list(user=username, repo=repo.name)
        my_repo_commits = filter(lambda s: s.author and s.author.login == username, repo_commits.iterator())
        all_commits.extend(list(my_repo_commits))
    return all_commits

def recent_commits(username, n=10):
    """Returns a list of recent commits by USERNAME. Each commit is represented
    as a Commit object."""
    return (Commit('hi'),) * n
    return tuple(Commit(c) for c in get_commits(username)[:n])

class Commit(object):
    def __init__(self, commit_object):
        self.message = commit_object
        self.committer = commit_object
        self.url = commit_object
        self.repo = commit_object
        self.date = commit_object
