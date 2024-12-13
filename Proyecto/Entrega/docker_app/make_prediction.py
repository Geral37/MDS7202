import pickle

# cargar modelo
with open('final_pipeline.pkl', 'rb') as file:
    model = pickle.load(file)

labels_dict = {0: 'No moroso', 1: 'Moroso'} # label dict
def make_prediction(borrow_block_number: int, borrow_timestamp: float, wallet_address: object, first_tx_timestamp: float, last_tx_timestamp: float, wallet_age: float, 
                    incoming_tx_count: int, outgoing_tx_count: int, net_incoming_tx_count: int, total_gas_paid_eth: float, avg_gas_paid_per_tx_eth: float, 
                    risky_tx_count: int, risky_unique_contract_count: int, risky_first_tx_timestamp: int, risky_last_tx_timestamp: int, 
                    risky_first_last_tx_timestamp_diff: int, risky_sum_outgoing_amount_eth: float, outgoing_tx_sum_eth: float, incoming_tx_sum_eth: float, 
                    outgoing_tx_avg_eth: float, incoming_tx_avg_eth: float, max_eth_ever: float, min_eth_ever: float, total_balance_eth: float, risk_factor: float, 
                    total_collateral_eth: float, total_collateral_avg_eth: float, total_available_borrows_eth: float, total_available_borrows_avg_eth: float, 
                    avg_weighted_risk_factor: float, risk_factor_above_threshold_daily_count: float, avg_risk_factor: float, max_risk_factor: float, 
                    borrow_amount_sum_eth: float, borrow_amount_avg_eth: float, borrow_count: int, repay_amount_sum_eth: float, repay_amount_avg_eth: float, 
                    repay_count: int, borrow_repay_diff_eth: float, deposit_count: int, deposit_amount_sum_eth: float, time_since_first_deposit: float, 
                    withdraw_amount_sum_eth: float, withdraw_deposit_diff_if_positive_eth: float, liquidation_count: int, time_since_last_liquidated: float, 
                    liquidation_amount_sum_eth: float, market_adx: float, market_adxr: float, market_apo: float, market_aroonosc: float, market_aroonup: float, 
                    market_atr: float, market_cci: float, market_cmo: float, market_correl: float, market_dx: float, market_fastk: float, market_fastd: float, 
                    market_ht_trendmode: int, market_linearreg_slope: float, market_macd_macdext: float, market_macd_macdfix: float, market_macd: float, 
                    market_macdsignal_macdext: float, market_macdsignal_macdfix: float, market_macdsignal: float, market_max_drawdown_365d: float, market_natr: float, 
                    market_plus_di: float, market_plus_dm: float, market_ppo: float, market_rocp: float, market_rocr: float, unique_borrow_protocol_count: int, 
                    unique_lending_protocol_count: int):
    '''
    función que devuelve la predicción del modelo dado un set de atributos
    '''

    # mantener el orden!
    features = [
        [borrow_block_number, borrow_timestamp, wallet_address, first_tx_timestamp, 
        last_tx_timestamp, wallet_age, incoming_tx_count, outgoing_tx_count, 
        net_incoming_tx_count, total_gas_paid_eth, avg_gas_paid_per_tx_eth, 
        risky_tx_count, risky_unique_contract_count, risky_first_tx_timestamp, 
        risky_last_tx_timestamp, risky_first_last_tx_timestamp_diff, 
        risky_sum_outgoing_amount_eth, outgoing_tx_sum_eth, incoming_tx_sum_eth, 
        outgoing_tx_avg_eth, incoming_tx_avg_eth, max_eth_ever, min_eth_ever, 
        total_balance_eth, risk_factor, total_collateral_eth, 
        total_collateral_avg_eth, total_available_borrows_eth, 
        total_available_borrows_avg_eth, avg_weighted_risk_factor, 
        risk_factor_above_threshold_daily_count, avg_risk_factor, max_risk_factor, 
        borrow_amount_sum_eth, borrow_amount_avg_eth, borrow_count, 
        repay_amount_sum_eth, repay_amount_avg_eth, repay_count, 
        borrow_repay_diff_eth, deposit_count, deposit_amount_sum_eth, 
        time_since_first_deposit, withdraw_amount_sum_eth, 
        withdraw_deposit_diff_if_positive_eth, liquidation_count, 
        time_since_last_liquidated, liquidation_amount_sum_eth, market_adx, 
        market_adxr, market_apo, market_aroonosc, market_aroonup, market_atr, 
        market_cci, market_cmo, market_correl, market_dx, market_fastk, 
        market_fastd, market_ht_trendmode, market_linearreg_slope, 
        market_macd_macdext, market_macd_macdfix, market_macd, 
        market_macdsignal_macdext, market_macdsignal_macdfix, market_macdsignal, 
        market_max_drawdown_365d, market_natr, market_plus_di, market_plus_dm, 
        market_ppo, market_rocp, market_rocr, unique_borrow_protocol_count, 
        unique_lending_protocol_count]  # obs to predict
    ]

    
    prediction = model.predict(features).item() # hacer prediccion
    label = labels_dict[prediction] # transformar a etiquetas

    return label # returnar prediccion