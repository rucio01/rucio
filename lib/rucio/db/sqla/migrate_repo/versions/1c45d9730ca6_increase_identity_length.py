'''
 Copyright European Organization for Nuclear Research (CERN)

 Licensed under the Apache License, Version 2.0 (the "License");
 You may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

 Authors:
 - Mario Lassnig, <mario.lassnig@cern.ch>, 2017

increase identity length

Revision ID: 1c45d9730ca6
Revises: c5c0418f31aa
Create Date: 2017-10-31 17:52:21.313035

'''
from alembic.op import alter_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c45d9730ca6'  # pylint: disable=invalid-name
down_revision = 'c5c0418f31aa'  # pylint: disable=invalid-name


def upgrade():
    '''
    upgrade method
    '''
    alter_column('tokens', 'identity',
                 existing_type=sa.String(255),
                 type_=sa.String(2048))
    alter_column('identities', 'identity',
                 existing_type=sa.String(255),
                 type_=sa.String(2048))
    alter_column('account_map', 'identity',
                 existing_type=sa.String(255),
                 type_=sa.String(2048))


def downgrade():
    '''
    downgrade method
    '''

    pass

    # attention!
    # we would have to delete all SSH  entries so we can shrink the colum.
    # since we don't want this to happen automatically, this downgrade is disabled

    # alter_column('tokens', 'identity',
    #              existing_type=sa.String(2048),
    #              type_=sa.String(255))
    # alter_column('identities', 'identity',
    #              existing_type=sa.String(2048),
    #              type_=sa.String(255))
    # alter_column('account_map', 'identity',
    #              existing_type=sa.String(2048),
    #              type_=sa.String(255))
