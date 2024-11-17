USE softeam;

-- Drop existing table for upstox instruments. A new one will be created and populated
DROP TABLE IF EXISTS upstox_instrument_data;

-- Table to store analyst data
CREATE TABLE IF NOT EXISTS softeam.trade_suggestion_analysis (
	id BIGINT auto_increment NOT NULL,
	suggestion_source varchar(100) NOT NULL,
	isin varchar(100) NOT NULL,
	trading_symnol varchar(100) NOT NULL,
	buying_price FLOAT NOT NULL,
	target_price FLOAT NOT NULL,
	stop_loss_price FLOAT NOT NULL,
	suggestion_timestamp TIMESTAMP NOT NULL,
    created_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT trade_suggestion_analysis_pk PRIMARY KEY (id)
);