from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
from make_prediction import make_prediction 

app = FastAPI()

# Endpoint para predecir desde CSV
@app.post("/predict_csv/")
async def predict_csv(file: UploadFile):
    df = pd.read_csv(file.file)  # Leer CSV
    # Asegurar que las columnas tengan los nombres esperados
    required_columns = ['borrow_block_number', 'borrow_timestamp', 'wallet_address', 'first_tx_timestamp', 'last_tx_timestamp', 'wallet_age', 'incoming_tx_count', 
                        'outgoing_tx_count', 'net_incoming_tx_count', 'total_gas_paid_eth', 'avg_gas_paid_per_tx_eth', 'risky_tx_count', 'risky_unique_contract_count', 
                        'risky_first_tx_timestamp', 'risky_last_tx_timestamp', 'risky_first_last_tx_timestamp_diff', 'risky_sum_outgoing_amount_eth', 
                        'outgoing_tx_sum_eth', 'incoming_tx_sum_eth', 'outgoing_tx_avg_eth', 'incoming_tx_avg_eth', 'max_eth_ever', 'min_eth_ever', 'total_balance_eth', 
                        'risk_factor', 'total_collateral_eth', 'total_collateral_avg_eth', 'total_available_borrows_eth', 'total_available_borrows_avg_eth', 
                        'avg_weighted_risk_factor', 'risk_factor_above_threshold_daily_count', 'avg_risk_factor', 'max_risk_factor', 'borrow_amount_sum_eth', 
                        'borrow_amount_avg_eth', 'borrow_count', 'repay_amount_sum_eth', 'repay_amount_avg_eth', 'repay_count', 'borrow_repay_diff_eth', 
                        'deposit_count', 'deposit_amount_sum_eth', 'time_since_first_deposit', 'withdraw_amount_sum_eth', 'withdraw_deposit_diff_if_positive_eth', 
                        'liquidation_count', 'time_since_last_liquidated', 'liquidation_amount_sum_eth', 'market_adx','market_adxr', 'market_apo', 'market_aroonosc', 
                        'market_aroonup', 'market_atr', 'market_cci', 'market_cmo', 'market_correl', 'market_dx', 'market_fastk', 'market_fastd', 'market_ht_trendmode', 
                        'market_linearreg_slope', 'market_macd_macdext', 'market_macd_macdfix', 'market_macd', 'market_macdsignal_macdext', 'market_macdsignal_macdfix', 
                        'market_macdsignal', 'market_max_drawdown_365d', 'market_natr', 'market_plus_di', 'market_plus_dm', 'market_ppo', 'market_rocp', 'market_rocr', 
                        'unique_borrow_protocol_count', 'unique_lending_protocol_count']

    if not all(col in df.columns for col in required_columns):
        return JSONResponse({"error": "El archivo no contiene las columnas necesarias"})

    # Generar predicciones
    df['Prediction'] = df.apply(
    lambda row: make_prediction(row['borrow_block_number'], row['borrow_timestamp'], row['wallet_address'], row['first_tx_timestamp'], row['last_tx_timestamp'], 
                                row['wallet_age'], row['incoming_tx_count'], row['outgoing_tx_count'], row['net_incoming_tx_count'], row['total_gas_paid_eth'],
                                row['avg_gas_paid_per_tx_eth'], row['risky_tx_count'], row['risky_unique_contract_count'], row['risky_first_tx_timestamp'],
                                row['risky_last_tx_timestamp'], row['risky_first_last_tx_timestamp_diff'], row['risky_sum_outgoing_amount_eth'],
                                row['outgoing_tx_sum_eth'], row['incoming_tx_sum_eth'], row['outgoing_tx_avg_eth'], row['incoming_tx_avg_eth'], row['max_eth_ever'],
                                row['min_eth_ever'], row['total_balance_eth'], row['risk_factor'], row['total_collateral_eth'], row['total_collateral_avg_eth'], 
                                row['total_available_borrows_eth'], row['total_available_borrows_avg_eth'], row['avg_weighted_risk_factor'], 
                                row['risk_factor_above_threshold_daily_count'], row['avg_risk_factor'], row['max_risk_factor'], row['borrow_amount_sum_eth'], 
                                row['borrow_amount_avg_eth'], row['borrow_count'], row['repay_amount_sum_eth'], row['repay_amount_avg_eth'], row['repay_count'],
                                row['borrow_repay_diff_eth'], row['deposit_count'], row['deposit_amount_sum_eth'], row['time_since_first_deposit'], 
                                row['withdraw_amount_sum_eth'], row['withdraw_deposit_diff_if_positive_eth'], row['liquidation_count'], row['time_since_last_liquidated'], 
                                row['liquidation_amount_sum_eth'], row['market_adx'], row['market_adxr'], row['market_apo'], row['market_aroonosc'], row['market_aroonup'], 
                                row['market_atr'], row['market_cci'], row['market_cmo'], row['market_correl'], row['market_dx'], row['market_fastk'], row['market_fastd'], 
                                row['market_ht_trendmode'], row['market_linearreg_slope'], row['market_macd_macdext'], row['market_macd_macdfix'], row['market_macd'], 
                                row['market_macdsignal_macdext'], row['market_macdsignal_macdfix'], row['market_macdsignal'], row['market_max_drawdown_365d'], 
                                row['market_natr'], row['market_plus_di'], row['market_plus_dm'], row['market_ppo'], row['market_rocp'], row['market_rocr'], 
                                row['unique_borrow_protocol_count'], row['unique_lending_protocol_count']), axis=1)


    output_file = "predictions.csv"
    df.to_csv(output_file, index=False)
    return FileResponse(output_file, media_type="text/csv", filename="predictions.csv")

# Endpoint para predecir manualmente
@app.post("/predict_manual/")

async def predict_manual(
    borrow_block_number: int = Form(...),
    borrow_timestamp: float = Form(...),
    wallet_address: str = Form(...),
    first_tx_timestamp: float = Form(...),
    last_tx_timestamp: float = Form(...),
    wallet_age: float = Form(...),
    incoming_tx_count: int = Form(...),
    outgoing_tx_count: int = Form(...),
    net_incoming_tx_count: int = Form(...),
    total_gas_paid_eth: float = Form(...),
    avg_gas_paid_per_tx_eth: float = Form(...),
    risky_tx_count: int = Form(...),
    risky_unique_contract_count: int = Form(...),
    risky_first_tx_timestamp: int = Form(...),
    risky_last_tx_timestamp: int = Form(...),
    risky_first_last_tx_timestamp_diff: int = Form(...),
    risky_sum_outgoing_amount_eth: float = Form(...),
    outgoing_tx_sum_eth: float = Form(...),
    incoming_tx_sum_eth: float = Form(...),
    outgoing_tx_avg_eth: float = Form(...),
    incoming_tx_avg_eth: float = Form(...),
    max_eth_ever: float = Form(...),
    min_eth_ever: float = Form(...),
    total_balance_eth: float = Form(...),
    risk_factor: float = Form(...),
    total_collateral_eth: float = Form(...),
    total_collateral_avg_eth: float = Form(...),
    total_available_borrows_eth: float = Form(...),
    total_available_borrows_avg_eth: float = Form(...),
    avg_weighted_risk_factor: float = Form(...),
    risk_factor_above_threshold_daily_count: float = Form(...),
    avg_risk_factor: float = Form(...),
    max_risk_factor: float = Form(...),
    borrow_amount_sum_eth: float = Form(...),
    borrow_amount_avg_eth: float = Form(...),
    borrow_count: int = Form(...),
    repay_amount_sum_eth: float = Form(...),
    repay_amount_avg_eth: float = Form(...),
    repay_count: int = Form(...),
    borrow_repay_diff_eth: float = Form(...),
    deposit_count: int = Form(...),
    deposit_amount_sum_eth: float = Form(...),
    time_since_first_deposit: float = Form(...),
    withdraw_amount_sum_eth: float = Form(...),
    withdraw_deposit_diff_if_positive_eth: float = Form(...),
    liquidation_count: int = Form(...),
    time_since_last_liquidated: float = Form(...),
    liquidation_amount_sum_eth: float = Form(...),
    market_adx: float = Form(...),
    market_adxr: float = Form(...),
    market_apo: float = Form(...),
    market_aroonosc: float = Form(...),
    market_aroonup: float = Form(...),
    market_atr: float = Form(...),
    market_cci: float = Form(...),
    market_cmo: float = Form(...),
    market_correl: float = Form(...),
    market_dx: float = Form(...),
    market_fastk: float = Form(...),
    market_fastd: float = Form(...),
    market_ht_trendmode: int = Form(...),
    market_linearreg_slope: float = Form(...),
    market_macd_macdext: float = Form(...),
    market_macd_macdfix: float = Form(...),
    market_macd: float = Form(...),
    market_macdsignal_macdext: float = Form(...),
    market_macdsignal_macdfix: float = Form(...),
    market_macdsignal: float = Form(...),
    market_max_drawdown_365d: float = Form(...),
    market_natr: float = Form(...),
    market_plus_di: float = Form(...),
    market_plus_dm: float = Form(...),
    market_ppo: float = Form(...),
    market_rocp: float = Form(...),
    market_rocr: float = Form(...),
    unique_borrow_protocol_count: int = Form(...),
    unique_lending_protocol_count: int = Form(...)
    ):
    # Usar make_prediction para generar la predicción
    prediction = make_prediction(borrow_block_number, borrow_timestamp, wallet_address, first_tx_timestamp, last_tx_timestamp, wallet_age, incoming_tx_count, 
                                 outgoing_tx_count, net_incoming_tx_count, total_gas_paid_eth, avg_gas_paid_per_tx_eth, risky_tx_count, risky_unique_contract_count,
                                 risky_first_tx_timestamp, risky_last_tx_timestamp, risky_first_last_tx_timestamp_diff, risky_sum_outgoing_amount_eth,
                                 outgoing_tx_sum_eth, incoming_tx_sum_eth, outgoing_tx_avg_eth, incoming_tx_avg_eth, max_eth_ever, min_eth_ever, total_balance_eth,
                                 risk_factor, total_collateral_eth, total_collateral_avg_eth, total_available_borrows_eth, total_available_borrows_avg_eth,
                                 avg_weighted_risk_factor, risk_factor_above_threshold_daily_count, avg_risk_factor, max_risk_factor, borrow_amount_sum_eth,
                                 borrow_amount_avg_eth, borrow_count, repay_amount_sum_eth, repay_amount_avg_eth, repay_count, borrow_repay_diff_eth,
                                 deposit_count, deposit_amount_sum_eth, time_since_first_deposit, withdraw_amount_sum_eth, withdraw_deposit_diff_if_positive_eth,
                                 liquidation_count, time_since_last_liquidated, liquidation_amount_sum_eth, market_adx, market_adxr, market_apo, market_aroonosc,
                                 market_aroonup, market_atr, market_cci, market_cmo, market_correl, market_dx, market_fastk, market_fastd, market_ht_trendmode,
                                 market_linearreg_slope, market_macd_macdext, market_macd_macdfix, market_macd, market_macdsignal_macdext, market_macdsignal_macdfix,
                                 market_macdsignal, market_max_drawdown_365d, market_natr, market_plus_di, market_plus_dm, market_ppo, market_rocp, market_rocr,
                                 unique_borrow_protocol_count, unique_lending_protocol_count)

    return JSONResponse({"prediction": prediction})

