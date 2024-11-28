USE softeam;

-- Drop existing table for upstox instruments. A new one will be created and populated
-- DROP TABLE IF EXISTS upstox_instrument_data;

-- Table to store analyst data
CREATE TABLE IF NOT EXISTS softeam.trade_suggestion_analysis (
	id BIGINT auto_increment NOT NULL,
	suggestion_source varchar(100) NOT NULL,
	isin varchar(100) NOT NULL,
	trading_symbol varchar(100) NOT NULL,
	buying_price FLOAT NOT NULL,
	target_price FLOAT NOT NULL,
	stop_loss_price FLOAT NOT NULL,
	suggestion_timestamp TIMESTAMP NOT NULL,
    created_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT trade_suggestion_analysis_pk PRIMARY KEY (id)
);

-- Table to store analysis results
CREATE TABLE softeam.trade_risk_analaysis (
	id BIGINT auto_increment NOT NULL,
	trading_symbol varchar(100) NOT NULL,
	buying_price FLOAT NOT NULL,
	target_price FLOAT NOT NULL,
	selling_price FLOAT NOT NULL,
	trade_suggestion_analysis_id BIGINT NULL,
	risk_parameter varchar(100) NOT NULL,
	evaluation_result FLOAT NULL,
	qualify_threshold BIT NOT NULL,
	created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT trade_risk_analaysis_pk PRIMARY KEY (id)
);

-- Table to store matching logic results
CREATE TABLE softeam.matching_logic_analysis (
	id BIGINT auto_increment NOT NULL,
	passed_company_name varchar(100) NOT NULL,
	clean_company_name varchar(100) NOT NULL,
	match_found BIT NOT NULL,
	matched_company_name varchar(100),
	fuzzy_score INT NULL,
	message varchar(500) NULL,
	trading_symbol varchar(100) NULL,
	isin varchar(100) NULL,
	created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT matching_logic_analysis_pk PRIMARY KEY (id)
);