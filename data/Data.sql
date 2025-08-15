use ecomdb
CREATE TABLE dbo.customers (
    customer_id     VARCHAR(64) PRIMARY KEY,
    country         NVARCHAR(100) NULL,
    first_purchase  DATETIME NULL,
    last_purchase   DATETIME NULL
);

CREATE TABLE dbo.products (
    product_id      VARCHAR(64) PRIMARY KEY,
    description     NVARCHAR(255) NULL,
    unit_price      DECIMAL(18,2) NULL
);

CREATE TABLE dbo.orders (
    order_id        VARCHAR(64) PRIMARY KEY,
    order_datetime  DATETIME NOT NULL,
    customer_id     VARCHAR(64) NOT NULL,
    CONSTRAINT FK_orders_customers FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id)
);

CREATE TABLE dbo.order_items (
    order_item_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_id        VARCHAR(64) NOT NULL,
    product_id      VARCHAR(64) NOT NULL,
    quantity        INT NOT NULL,
    unit_price      DECIMAL(18,2) NOT NULL,
    CONSTRAINT FK_items_orders FOREIGN KEY (order_id) REFERENCES dbo.orders(order_id),
    CONSTRAINT FK_items_products FOREIGN KEY (product_id) REFERENCES dbo.products(product_id)
);

-- RFM & phân khúc
CREATE TABLE dbo.customer_rfm (
    customer_id     VARCHAR(64) PRIMARY KEY,
    recency_days    INT NOT NULL,
    frequency       INT NOT NULL,
    monetary        DECIMAL(18,2) NOT NULL,
    r_score         TINYINT NULL,
    f_score         TINYINT NULL,
    m_score         TINYINT NULL,
    segment_label   NVARCHAR(50) NULL,
    updated_at      DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_rfm_customers FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id)
);

-- Lưu gợi ý Top-N
CREATE TABLE dbo.recommendations (
    customer_id     VARCHAR(64) NOT NULL,
    product_id      VARCHAR(64) NOT NULL,
    rank_order      INT NOT NULL,
    score           FLOAT NULL,
    created_at      DATETIME NOT NULL DEFAULT GETDATE(),
    PRIMARY KEY (customer_id, product_id),
    CONSTRAINT FK_reco_customers FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id),
    CONSTRAINT FK_reco_products FOREIGN KEY (product_id) REFERENCES dbo.products(product_id)
);
