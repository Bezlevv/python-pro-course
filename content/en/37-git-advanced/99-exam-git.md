---
title: Exam: Advanced Git
summary: Test your knowledge of advanced Git: rebase, cherry-pick, conflicts, reflog, bisect, hooks, remote strategies and worktree.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What does git rebase main do (while on branch feature)?
- Creates a merge commit
- Moves feature commits on top of the tip of main
- Deletes branch main
- Copies files from main into feature
* Correct answer: Moves feature commits on top of the tip of main
Rebase cuts the commits of the current branch and applies them again on top of the given base, making history linear.

Why must you not rebase already published commits?
- It is slow
- Other participants will get divergent histories and conflicts
- Git forbids it forever
- The commits will disappear from the reflog
* Correct answer: Other participants will get divergent histories and conflicts
Rewriting shared commits breaks history for those who already downloaded them.

What should you do with the markers when resolving a conflict?
- Leave them in the file
- Delete all three markers and keep the needed variant
- Turn them into comments
- Move them to the end of the file
* Correct answer: Delete all three markers and keep the needed variant
The markers are auxiliary markup: after choosing a variant they must be deleted.

What does --theirs mean in git merge?
- The variant of the current branch into which changes are being merged
- The variant of the branch being merged in
- The variant from the index
- The variant from the stash
* Correct answer: The variant of the branch being merged in
In merge ours is the current branch, theirs is the merged-in branch. In rebase the roles swap.

What does git reflog store?
- Only deleted branches
- The history of all HEAD movements: commits, checkout, reset, merge, rebase
- The content of all files
- Passwords and access keys
* Correct answer: The history of all HEAD movements: commits, checkout, reset, merge, rebase
Every change of the HEAD pointer is recorded in the reflog with a timestamp and a description of the action.

What does git fsck --lost-found return?
- A list of dangling objects nobody references
- A list of all repository branches
- A list of configured remotes
- A list of conflicting files
* Correct answer: A list of dangling objects nobody references
Commits without references are found via fsck; they can be restored by hash.

What does the pre-commit hook do?
- Runs before a commit is created and can block it
- Runs after push
- Checks the commit message
- Creates branches
* Correct answer: Runs before a commit is created and can block it
pre-commit runs before the commit is written; a non-zero code cancels the commit.

How does --force-with-lease differ from --force?
- It first checks that the remote branch has not changed since the last fetch
- It only works with bare repositories
- It does not allow rewriting history at all
- It requires explicit confirmation
* Correct answer: It first checks that the remote branch has not changed since the last fetch
If someone managed to push, --force-with-lease refuses, while bare --force wipes other people's work.

What does git worktree add ../fix -b hotfix/fix create?
- A new working copy on a new branch
- A clone of the whole repository
- A bare repository
- A new remote
* Correct answer: A new working copy on a new branch
Worktree adds another working tree of the same repository on the given branch.

How to correctly move a fix from hotfix to main and release?
- git cherry-pick <sha_fix> in both branches
- git rebase hotfix
- git merge --no-ff main
- git reset --hard <sha_fix>
* Correct answer: git cherry-pick <sha_fix> in both branches
cherry-pick applies a specific commit in each branch separately without dragging the rest of history.

<!--/QUIZ-->
