# -*- coding: utf-8 -*-

import cProfile
import os.path

from outwiker.core.system import getSpecialDirList


def profile(func):
    '''
    Decorator to profile function
    '''
    def new_func(*args, **kwargs):
        profile_dir = getSpecialDirList('.')[-1]
        profile_name = 'profile_{}'.format(func.__name__)
        profile_path = os.path.join(profile_dir, profile_name)

        profile = cProfile.Profile()
        profile.enable()
        func(*args, **kwargs)
        profile.create_stats()
        profile.dump_stats(profile_path)

    return new_func
