"""podcasts table

Revision ID: 95109fae6ab2
Revises: 
Create Date: 2022-01-23 14:28:22.110959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95109fae6ab2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('podcast',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('s3_foldername', sa.String(length=120), nullable=True),
    sa.Column('s3_bucket', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_podcast_description'), 'podcast', ['description'], unique=False)
    op.create_index(op.f('ix_podcast_s3_bucket'), 'podcast', ['s3_bucket'], unique=False)
    op.create_index(op.f('ix_podcast_s3_foldername'), 'podcast', ['s3_foldername'], unique=False)
    op.create_index(op.f('ix_podcast_title'), 'podcast', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_podcast_title'), table_name='podcast')
    op.drop_index(op.f('ix_podcast_s3_foldername'), table_name='podcast')
    op.drop_index(op.f('ix_podcast_s3_bucket'), table_name='podcast')
    op.drop_index(op.f('ix_podcast_description'), table_name='podcast')
    op.drop_table('podcast')
    # ### end Alembic commands ###
