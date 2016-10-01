# -*- coding: UTF-8 -*-


def checkVersion(packageversion, required):
    '''
    Return True if version satisfies the requirement.
    packageversion and required - tuples of the form (1, 0), (2, 10) etc.

    The first items of the tuples must be equal. The second item of the
    packageversion tuple must be great or equal the second item of the
    required tuple.
    '''
    return (packageversion[0] == required[0] and
            packageversion[1] >= required[1])
