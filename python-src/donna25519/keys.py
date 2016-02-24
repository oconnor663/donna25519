'''
LICENSING
-------------------------------------------------

Copyright (c) 2016, Muterra Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Muterra Inc nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL MUTERRA INC BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------

Modified from code originally written by Brian Warner.
'''

from . import _curve25519
from hashlib import sha256
import os

# the curve25519 functions are really simple, and could be used without an
# OOP layer, but it's a bit too easy to accidentally swap the private and
# public keys that way.

def _hash_shared(shared):
    return sha256(b"curve25519-shared:"+shared).digest()

class Private():
    def __init__(self, secret=None):
        # Generate secret if none is passed
        if secret is None:
            secret = os.urandom(32)
        
        # Try and catch
        try:
            self._private = _curve25519.make_private(secret)
        except TypeError as e:
            raise TypeError('Secret must be more bytes-like (try bytes).')
        
    @property
    def private(self):
        ''' Read-only to help insulate accidental deletions.
        '''
        return self._private

    def get_public(self):
        return Public(_curve25519.make_public(self.private))

    def get_shared_key(self, public, hashfunc=None):
        if not isinstance(public, Public):
            raise ValueError("'public' must be an instance of Public")
        if hashfunc is None:
            hashfunc = _hash_shared
        shared = _curve25519.make_shared(self.private, public.public)
        return hashfunc(shared)

class Public():
    def __init__(self, public):
        assert isinstance(public, bytes)
        assert len(public) == 32
        self._public = public
        
    @property
    def public(self):
        ''' Read-only to help insulate accidental deletions.
        '''
        return self._public