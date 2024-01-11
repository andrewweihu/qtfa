import qtc.utils.misc_utils as mu
import qtc.utils.db_utils as dbu
import qtc.data.dal.common.sql_compiler as sqlc


def query_money_flow(start_dateid=None, end_dateid=None, dateids=None,
                     security_codes=None,
                     cols=None,
                     database='CN-EQUITY-VENDOR',
                     **db_config):
    """
    >>> import qtfa.data.dal.factor as dalf
    >>> dalf.query_money_flow(security_codes='600693.SH,000001.SZ', dateids=20230519)
       trade_date    ts_code  buy_sm_vol  buy_sm_amount  sell_sm_vol  sell_sm_amount  buy_md_vol  buy_md_amount  sell_md_vol  sell_md_amount  buy_lg_vol  buy_lg_amount  sell_lg_vol  sell_lg_amount  buy_elg_vol  buy_elg_amount  sell_elg_vol  sell_elg_amount  net_mf_vol  net_mf_amount             UpdateDateTime
    0    20230519  000001.SZ    182437.0       22551.65     145443.0        17990.39    196863.0       24339.37     186742.0        23092.77    204460.0       25288.67     189440.0        23429.55     104654.0        12936.87      166788.0         20603.84   -143350.0      -17682.92 2023-05-25 02:01:30.390232
    1    20230519  600693.SH     23472.0         938.22      19638.0          784.61     10453.0         417.45      10187.0          407.29      3145.0         125.57       6262.0          250.09          0.0            0.00         984.0            39.25     -1623.0         -63.36 2023-05-25 02:01:30.390232
    """
    sql_and_clauses = list()
    if security_codes is not None:
        security_codes_db_str = mu.iterable_to_db_str(security_codes, raw_type='str')
        sql_and_clauses.append(f'"ts_code" IN {security_codes_db_str}')

    dateid_sql_and_clauses = sqlc.build_dateid_sql_and_clauses(
        start_dateid=start_dateid, end_dateid=end_dateid, dateids=dateids,
        quotes_on_colnames=True
    )
    dateid_sql_and_clauses = [s.replace('DateId','trade_date') for s in dateid_sql_and_clauses]
    sql_and_clauses.extend(dateid_sql_and_clauses)

    sql = f'''
        SELECT * FROM "tushare"."DailyMoneyFlow"
        {dbu.compile_sql_where_clause(sql_and_clauses)}
    '''

    conn = dbu.get_os_env_conn(database=database,
                               **db_config)
    required_cols = ['trade_date','ts_code']
    money_flow = dbu.sql2df(sql=sql, conn=conn,
                            required_cols=required_cols, cols=cols,
                            preprocess_cols=False,
                            quotes_on_colnames=True)
    return money_flow


def query_basic(start_dateid=None, end_dateid=None, dateids=None,
                security_codes=None,
                cols=None,
                database='CN-EQUITY-VENDOR',
                **db_config):
    """
    >>> import qtfa.data.dal.factor as dalf
    >>> dalf.query_basic(security_codes='600693.SH,000001.SZ', dateids=20230519, cols='circ_mv')
       trade_date    ts_code       circ_mv
    0    20230519  000001.SZ  2.394644e+07
    1    20230519  600693.SH  3.475459e+05
    """
    sql_and_clauses = list()
    if security_codes is not None:
        security_codes_db_str = mu.iterable_to_db_str(security_codes, raw_type='str')
        sql_and_clauses.append(f'"ts_code" IN {security_codes_db_str}')

    dateid_sql_and_clauses = sqlc.build_dateid_sql_and_clauses(
        start_dateid=start_dateid, end_dateid=end_dateid, dateids=dateids,
        quotes_on_colnames=True
    )
    dateid_sql_and_clauses = [s.replace('DateId','trade_date') for s in dateid_sql_and_clauses]
    sql_and_clauses.extend(dateid_sql_and_clauses)

    sql = f'''
        SELECT * FROM "tushare"."DailyBasic"
        {dbu.compile_sql_where_clause(sql_and_clauses)}
    '''

    conn = dbu.get_os_env_conn(database=database,
                               **db_config)
    required_cols = ['trade_date','ts_code']
    basic = dbu.sql2df(sql=sql, conn=conn,
                       required_cols=required_cols, cols=cols,
                       preprocess_cols=False,
                       quotes_on_colnames=True)
    return basic
