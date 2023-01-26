from datetime import datetime
import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from cashflows.models import Cashflow
from buildings.models import Building


def calculate(
    cashflow_qs=Cashflow.objects.filter(building__id=4),
    building_qs=Building.objects.all(), groupby=False
):
    start_time = datetime.now()
    print(start_time)
    print('Recalculating...')
    cashflow_df = read_frame(cashflow_qs, verbose=False)
    print(cashflow_df.shape)
    building_df = read_frame(building_qs, verbose=False)
    cashflow_df['value'] = cashflow_df['value'].astype('float')
    t = np.arange('2020-04', '2046-04', 3, dtype='datetime64[M]')
    base_fy_start = 2020
    y = np.arange(0, len(cashflow_df))
    period_start = np.tile(t, len(y))
    period_end = period_start + np.timedelta64(3, 'M') - np.timedelta64(1, 'D')
    period_dur = (period_end - period_start + 1).astype(int)
    year = period_start.astype('datetime64[Y]').astype(int) + 1970
    month = period_start.astype('datetime64[M]').astype(int) % 12 + 1
    fy_start = np.where(month != 1, year, year - 1)
    time_index = fy_start - base_fy_start
    cross_index = np.repeat(y, len(t))
    start = cashflow_df['start'].values.astype('datetime64[D]')
    end = cashflow_df['end'].values.astype('datetime64[D]')
    start = np.repeat(start, len(t))
    end = np.repeat(end, len(t))
    span = (np.minimum(period_end, end) -
            np.maximum(period_start, start)).astype(int)
    span = np.where(span >= 0, span + 1, span)
    period_frac = span / period_dur
    lump_sum = np.where(start == end, True, False)
    vector_list = [period_start, period_end, period_dur,
                   fy_start, time_index, cross_index, period_frac, lump_sum]
    data_array = np.transpose(vector_list)
    column_list = [
        'period_start', 'period_end', 'period_dur',
        'fy_start', 'time_index', 'cross_index', 'period_frac', 'lump_sum'
    ]
    df = pd.DataFrame(data=data_array, columns=column_list)
    in_date_condition = df['period_frac'] > 0
    df = df[in_date_condition]
    df = df.merge(cashflow_df, left_on='cross_index', right_index=True)
    df = df.merge(building_df, left_on='building', right_index=True)
    df['fy_string'] = (
        df['fy_start'].map(str) + '/' + (df['fy_start'] + 1).map(str)
    )
    df['value_norm'] = (df['value'] / 4).where(~df['lump_sum'], df['value'])
    df['value_norm'] = (
        (df['value_norm'] * df['period_frac'])
        .where(~df['lump_sum'], df['value_norm'])
    )
    if groupby:
        df = df.groupby(groupby, as_index=False).agg({'value_norm': 'sum'})
    data = df.to_dict('records')
    print(df.columns)
    print(f'Rows, Columns = {df.shape}')
    print(f'Datapoints = {df.size}')
    print('Calculation Complete!')
    duration = datetime.now() - start_time
    print(f'Duration: {duration}')

    return data
