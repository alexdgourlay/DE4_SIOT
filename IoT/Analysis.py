# def Causality():
#     rows = 5
#     fig, ax = plt.subplots(nrows=rows, ncols=2)
#     ax = [item for sublist in ax for item in sublist]

#     lag = 80
#     idx = 0

#     for coin in cmc_df.columns[1:rows+1]:

#         ax[idx].plot(twitter_df.index[1:], np.diff(twitter_df[coin]))
#         ax[idx].twinx().plot(cmc_df.index, cmc_df[coin], color='green')

#         FormatTimeAxis(ax[idx].xaxis, 12)
#         idx += 1

#         array = [cmc_df[coin].values[1:], np.diff(twitter_df[coin].values)]
#         array = np.asarray(array).transpose()

#         gc_test = grangercausalitytests(array, maxlag=lag, verbose=False)
#         pvals = [gc_test.get(i+1)[0].get('ssr_ftest')[1]
#                  for i in range(0, lag)]

#         ax[idx].plot(pvals)

#         idx += 1

#     fig.autofmt_xdate()

# def auto():
#     coin = 'bitcoin'
#     fig = plt.figure()
#     fig.add_subplot(121)
#     plot_acf(np.diff(twitter_df[coin].values), lags=10)
#     fig.add_subplot(122)
#     plot_acf(np.diff(twitter_df[coin].values), lags=10)