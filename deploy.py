#!/bin/python

import deploy_jenkins, deploy_git

BRANCH_BASE = "commcare_"

def create_release():
    """
    Cuts release git branches from master and creates new jenkins release jobs.
    """
    version = deploy_jenkins.create_new_release_jobs()
    deploy_git.create_new_branches(BRANCH_BASE, version)

def deploy_release():
    """
    Creates minor release tags from release branch and updates jenkins jobs to
    build from that tag.
    """
    version = deploy_jenkins.get_staged_release_version()
    tag = deploy_git.schedule_minor_release(BRANCH_BASE, version)
    branch = '{}{}'.format(BRANCH_BASE, version.short_string())
    deploy_jenkins.make_release_jobs_use_tags(branch, tag)
    print("Now go name the resulting build to {} and mark it to keep around forever".format(tag))
    print("Then run update_hotfix_release_version")

def update_hotfix_release_version():
    """
    Increments the hotfix number on the latest commcare-mobile release job so
    it is ready for the next hotfix.
    """
    version = deploy_jenkins.get_staged_release_version()
    deploy_jenkins.inc_hotfix_version(version)

def create_hotfix():
    """
    Re-open release branch from latest release branch and update release jobs
    to build against those branches.
    """
    version = deploy_jenkins.get_staged_release_version()

    old_tag = "{}{}".format(BRANCH_BASE, version.get_last_hotfix())
    branch = "{}{}".format(BRANCH_BASE, version.short_string())

    deploy_git.checkout_old_tag(old_tag)
    deploy_jenkins.build_jobs_against_branch(branch)

def deploy_hotfix():
    """
    Finalize hotfix by creating its tags and setting the release jobs to build
    off them
    """
    version = deploy_jenkins.get_staged_release_version()
    tag = deploy_git.schedule_hotfix_release(BRANCH_BASE, version)
    deploy_jenkins.inc_hotfix_version(version)
