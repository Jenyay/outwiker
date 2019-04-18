# -*- coding: utf-8 -*-

import cProfile
import os.path

from outwiker.core.system import getSpecialDirList


def profile(prefix):
    def profile_decorator(func):
        '''
        Decorator to profile function
        '''
        def new_func(*args, **kwargs):
            profile_dir = getSpecialDirList('.')[-1]
            profile_name = 'profile_{}{}'.format(prefix, func.__name__)
            profile_path = os.path.join(profile_dir, profile_name)

            profile = cProfile.Profile()
            profile.enable()
            result = func(*args, **kwargs)
            profile.create_stats()
            profile.dump_stats(profile_path)
            return result

        return new_func

    return profile_decorator
