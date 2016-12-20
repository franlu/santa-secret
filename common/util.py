#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools


def pairing(giver, receiver):
    for g, r in itertools.izip_longest(giver, receiver):
        if g == r:
            return False
    return True
