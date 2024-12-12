import gradio as gr
import requests

# Función para enviar CSV
def predict_csv(file):
    response = requests.post(
        "http://127.0.0.1:8000/predict_csv/", 
        files={"file": file}
    )
    with open("output.csv", "wb") as f:
        f.write(response.content)
    return "output.csv"

# Función para enviar datos manuales
def predict_manual(sepal_length, sepal_width, petal_length, petal_width):
    response = requests.post(
        "http://127.0.0.1:8000/predict_manual/",
        data={
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        }
    )
    return response.json()["prediction"]

# Interfaz de Gradio
with gr.Blocks() as demo:
    gr.Markdown("# De las Comisiones a la Innovación: El Giro de Ignacio Yacurro")
    gr.Markdown("### Predicción de morosidad por el equipo Ratas.py 🐁")
    
    with gr.Tab("Cargar CSV"):
        csv_input = gr.File(label="Carga tu archivo CSV")
        csv_output = gr.File(label="Predicciones (archivo CSV)")
        csv_button = gr.Button("Predecir")
        csv_button.click(predict_csv, inputs=csv_input, outputs=csv_output)
    


    with gr.Tab("Ingresar datos manualmente"):
        borrow_block_number = gr.Number(label="Borrow Block Number", precision=0)
        borrow_timestamp = gr.Number(label="Borrow Timestamp")
        wallet_address = gr.Textbox(label="Wallet Address")
        first_tx_timestamp = gr.Number(label="First Transaction Timestamp")
        last_tx_timestamp = gr.Number(label="Last Transaction Timestamp")
        wallet_age = gr.Number(label="Wallet Age")
        incoming_tx_count = gr.Number(label="Incoming Transaction Count", precision=0)
        outgoing_tx_count = gr.Number(label="Outgoing Transaction Count", precision=0)
        net_incoming_tx_count = gr.Number(label="Net Incoming Transaction Count", precision=0)
        total_gas_paid_eth = gr.Number(label="Total Gas Paid (ETH)")
        avg_gas_paid_per_tx_eth = gr.Number(label="Average Gas Paid Per Transaction (ETH)")
        risky_tx_count = gr.Number(label="Risky Transaction Count", precision=0)
        risky_unique_contract_count = gr.Number(label="Risky Unique Contract Count", precision=0)
        risky_first_tx_timestamp = gr.Number(label="Risky First Transaction Timestamp", precision=0)
        risky_last_tx_timestamp = gr.Number(label="Risky Last Transaction Timestamp", precision=0)
        risky_first_last_tx_timestamp_diff = gr.Number(label="Risky First-Last Tx Timestamp Diff", precision=0)
        risky_sum_outgoing_amount_eth = gr.Number(label="Risky Sum of Outgoing Amount (ETH)")
        outgoing_tx_sum_eth = gr.Number(label="Outgoing Transaction Sum (ETH)")
        incoming_tx_sum_eth = gr.Number(label="Incoming Transaction Sum (ETH)")
        outgoing_tx_avg_eth = gr.Number(label="Average Outgoing Transaction (ETH)")
        incoming_tx_avg_eth = gr.Number(label="Average Incoming Transaction (ETH)")
        max_eth_ever = gr.Number(label="Max ETH Ever")
        min_eth_ever = gr.Number(label="Min ETH Ever")
        total_balance_eth = gr.Number(label="Total Balance (ETH)")
        risk_factor = gr.Number(label="Risk Factor")
        total_collateral_eth = gr.Number(label="Total Collateral (ETH)")
        total_collateral_avg_eth = gr.Number(label="Average Collateral (ETH)")
        total_available_borrows_eth = gr.Number(label="Total Available Borrows (ETH)")
        total_available_borrows_avg_eth = gr.Number(label="Average Available Borrows (ETH)")
        avg_weighted_risk_factor = gr.Number(label="Average Weighted Risk Factor")
        risk_factor_above_threshold_daily_count = gr.Number(label="Risk Factor Above Threshold (Daily Count)")
        avg_risk_factor = gr.Number(label="Average Risk Factor")
        max_risk_factor = gr.Number(label="Max Risk Factor")
        borrow_amount_sum_eth = gr.Number(label="Borrow Amount Sum (ETH)")
        borrow_amount_avg_eth = gr.Number(label="Average Borrow Amount (ETH)")
        borrow_count = gr.Number(label="Borrow Count", precision=0)
        repay_amount_sum_eth = gr.Number(label="Repay Amount Sum (ETH)")
        repay_amount_avg_eth = gr.Number(label="Average Repay Amount (ETH)")
        repay_count = gr.Number(label="Repay Count", precision=0)
        borrow_repay_diff_eth = gr.Number(label="Borrow-Repay Difference (ETH)")
        deposit_count = gr.Number(label="Deposit Count", precision=0)
        deposit_amount_sum_eth = gr.Number(label="Deposit Amount Sum (ETH)")
        time_since_first_deposit = gr.Number(label="Time Since First Deposit")
        withdraw_amount_sum_eth = gr.Number(label="Withdraw Amount Sum (ETH)")
        withdraw_deposit_diff_if_positive_eth = gr.Number(label="Withdraw-Deposit Difference (if Positive) (ETH)")
        liquidation_count = gr.Number(label="Liquidation Count", precision=0)
        time_since_last_liquidated = gr.Number(label="Time Since Last Liquidation")
        liquidation_amount_sum_eth = gr.Number(label="Liquidation Amount Sum (ETH)")
        market_adx = gr.Number(label="Market ADX")
        market_adxr = gr.Number(label="Market ADXR")
        market_apo = gr.Number(label="Market APO")
        market_aroonosc = gr.Number(label="Market Aroon Oscillator")
        market_aroonup = gr.Number(label="Market Aroon Up")
        market_atr = gr.Number(label="Market ATR")
        market_cci = gr.Number(label="Market CCI")
        market_cmo = gr.Number(label="Market CMO")
        market_correl = gr.Number(label="Market Correlation")
        market_dx = gr.Number(label="Market DX")
        market_fastk = gr.Number(label="Market FastK")
        market_fastd = gr.Number(label="Market FastD")
        market_ht_trendmode = gr.Number(label="Market HT Trend Mode", precision=0)
        market_linearreg_slope = gr.Number(label="Market Linear Regression Slope")
        market_macd_macdext = gr.Number(label="Market MACD Extension")
        market_macd_macdfix = gr.Number(label="Market MACD Fixed")
        market_macd = gr.Number(label="Market MACD")
        market_macdsignal_macdext = gr.Number(label="Market MACD Signal Extension")
        market_macdsignal_macdfix = gr.Number(label="Market MACD Signal Fixed")
        market_macdsignal = gr.Number(label="Market MACD Signal")
        market_max_drawdown_365d = gr.Number(label="Market Max Drawdown (365d)")
        market_natr = gr.Number(label="Market NATR")
        market_plus_di = gr.Number(label="Market Plus DI")
        market_plus_dm = gr.Number(label="Market Plus DM")
        market_ppo = gr.Number(label="Market PPO")
        market_rocp = gr.Number(label="Market ROCP")
        market_rocr = gr.Number(label="Market ROCR")
        unique_borrow_protocol_count = gr.Number(label="Unique Borrow Protocol Count", precision=0)
        unique_lending_protocol_count = gr.Number(label="Unique Lending Protocol Count", precision=0)
        
        prediction_output = gr.Textbox(label="Predicción")
        manual_button = gr.Button("Predecir")
        
        manual_button.click(
            predict_manual,
            inputs=[
                borrow_block_number, borrow_timestamp, wallet_address, first_tx_timestamp, last_tx_timestamp, wallet_age,
                incoming_tx_count, outgoing_tx_count, net_incoming_tx_count, total_gas_paid_eth, avg_gas_paid_per_tx_eth,
                risky_tx_count, risky_unique_contract_count, risky_first_tx_timestamp, risky_last_tx_timestamp,
                risky_first_last_tx_timestamp_diff, risky_sum_outgoing_amount_eth, outgoing_tx_sum_eth, incoming_tx_sum_eth,
                outgoing_tx_avg_eth, incoming_tx_avg_eth, max_eth_ever, min_eth_ever, total_balance_eth, risk_factor,
                total_collateral_eth, total_collateral_avg_eth, total_available_borrows_eth, total_available_borrows_avg_eth,
                avg_weighted_risk_factor, risk_factor_above_threshold_daily_count, avg_risk_factor, max_risk_factor,
                borrow_amount_sum_eth, borrow_amount_avg_eth, borrow_count, repay_amount_sum_eth, repay_amount_avg_eth,
                repay_count, borrow_repay_diff_eth, deposit_count, deposit_amount_sum_eth, time_since_first_deposit,
                withdraw_amount_sum_eth, withdraw_deposit_diff_if_positive_eth, liquidation_count, time_since_last_liquidated,
                liquidation_amount_sum_eth, market_adx, market_adxr, market_apo, market_aroonosc, market_aroonup, market_atr,
                market_cci, market_cmo, market_correl, market_dx, market_fastk, market_fastd, market_ht_trendmode,
                market_linearreg_slope, market_macd_macdext, market_macd_macdfix, market_macd, market_macdsignal_macdext,
                market_macdsignal_macdfix, market_macdsignal, market_max_drawdown_365d, market_natr, market_plus_di,
                market_plus_dm, market_ppo, market_rocp, market_rocr, unique_borrow_protocol_count, unique_lending_protocol_count
            ],
            outputs=prediction_output
        )


demo.launch()

