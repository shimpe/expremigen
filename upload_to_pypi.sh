#!/usr/bin/env bash
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "there are uncommitted changes";
else
    echo "all local changes are committed (didn't check for new files!)";
    rm dist/*.tar.gz
    echo "Make sure you've increased the version number in setup.py. Then, type that version here (e.g. 1.1.4), followed by [ENTER]:"
    read -e tag
    git tag "$tag" -m "tag version $tag"
    git push --tags origin master
    python setup.py sdist
    twine upload dist/*
fi

