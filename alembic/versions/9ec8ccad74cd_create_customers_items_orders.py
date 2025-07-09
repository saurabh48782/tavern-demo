"""create customers, items, orders

Revision ID: 9ec8ccad74cd
Revises:
Create Date: 2025-04-20 03:36:12.496478

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9ec8ccad74cd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL
        );

        CREATE TABLE items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price NUMERIC NOT NULL,
            in_stock BOOLEAN DEFAULT TRUE
        );

        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE order_items (
            order_id INTEGER REFERENCES orders(id),
            item_id INTEGER REFERENCES items(id),
            PRIMARY KEY (order_id, item_id)
        );
    """)
    pass


def downgrade() -> None:
    op.execute("""
        DROP TABLE order_items;
        DROP TABLE orders;
        DROP TABLE items;
        DROP TABLE customers;
    """)
    pass
