# Contribution Guidelines

## Overview
* **"First-timers" are welcome!** Whether you're trying to learn data science, hone your coding skills, or get started collaborating over the web, we're happy to help. *(Sidenote: with respect to Git and GitHub specifically, our [github-playground](https://github.com/Data4Democracy/github-playground) repo and the [#github-help](https://datafordemocracy.slack.com/messages/github-help/) Slack channel are good places to start.)*
* **We believe good code is reviewed code.** All commits to this repository are approved by project maintainers and/or leads (listed above). The goal here is *not* to criticize or judge your abilities! Rather, sharing insights and achievements. Code reviews help us continually refine the project's scope and direction, as well as encourage the discussion we need for it to thrive.
* **Get involved!** Browse our [help wanted issues](https://github.com/Data4Democracy/immigration-connect/issues). All of our current discussions, proposals, and active projects are kept there and it will be the fastest way to determine how you can jump in and start helping. See if there is anything that interests you, start commenting here or in the [Slack channel](https://datafordemocracy.slack.com/messages/immigration-connect/), and you can start contributing right away!

## Git Workflow

This project uses a "Fork & Pull" git model. This means the `D4D` organization maintains the canonical repositories and issue tracking.
To begin contributing for the first time, you must _fork_ the repository.

### Workflow

1. Assign yourself to an issue from the project or ping @jtorrez to assign it to you. If there isn't an open issue for what you'd like to contribute, please open one so we can track the idea and discussion.
2. Ensure your local repository's `master` branch is up-to-date with the canonical `master`.

```
$ git fetch upstream master
$ git checkout master
$ git merge upstream/master
```

NOTE: the `merge` operation above should actually just be a fast-forward (i.e. the `master` branch is ahead of your copy of the master branch) merge. If it is not, somehow your master branch has diverged from the canonical master. In this case, you should make a new branch as a backup, delete master, and recreate it.

```
$ git checkout -b backup
$ git branch -d master
$ git checkout upstream/master
```

3. Create a new topic branch off of master. This branch is where you will commit work for the issue you are working. It should be descriptive but succinct. Because all work should have an issue first, the branch should take include the issue number, i.e. `issue#-issue-title`

```
$ git checkout -b 23-new-feature
```

4. Commit your work as you go. Commit messages should:
* Contain a first line summary, less than 50 chars
* Summary must begin with an imperative verb, i.e. "fix", "add", "change"
* Summary line should **NOT** end with a period. It's a title. Title's don't end in a period.
* Second line is always blank
* More detailed information can be added after the second line, if necessary. It should be manually line-breaked at around 72 chars.

5. Occasionally (or regularly) push your topic branch to **YOUR** fork.

```
$ git push origin 23-new-feature
```

6. When you are done working on an issue, or otherwise need to solicit feedback, create a merge request (or pull request) between your topic branch and the master branch in Qntfy's canonical repository. The merge request should include a `#`, the issue number in the beginning of the name, followed by a colon. i.e. `#24: Add DACA visualization`.The `#24` will allow us to easily associate a PR with the issue you are working on.

7. Go through the code review process. Team leads and collaborators have write access and will merge your contribution when it passes the review process.

8. Give yourself a high five, you just contributed to a D4D repository!
