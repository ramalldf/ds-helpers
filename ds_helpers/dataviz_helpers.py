import pandas as pd
import  numpy  as  np
import  matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import auc

def plot_pairs(input_df, target_col, grid_col_num):
    '''Use Seaborn to plot the relationships between feat cols against one
    target column. Define number of columns in plot grid with grid_col_num'''
    
    # Define dimensions of grid
    feat_cols_only = input_df.drop(target_col, axis=1).columns
    n_cols = grid_col_num
    n_rows = len(feat_cols_only)//n_cols
    print(len(feat_cols_only), n_rows)
    
    # Split feats list into sublists to match grid dimensions
    splits = np.array_split(feat_cols_only, n_rows)
    splits = splits[::-1]
    
    # Plot pair based on these target and sublists of features
    for i in splits:
        sns.pairplot(input_df, y_vars=target_col, x_vars=i)
    


def scatter_boxplot(my_df, xlabels, ylabels, title, fig_size= [10,6]):
    '''Style formatting for boxplots'''

    plt.subplots(1,1, figsize=fig_size, facecolor='white')
    plt.style.use('fivethirtyeight')
    sns.boxplot(data=my_df, saturation= 0.2)
    sns.stripplot(data=my_df, jitter=True, size= 8.5, linewidth= 1, edgecolor= 'black')
    plt.xlabel(xlabels, fontsize=20, fontweight='bold')
    plt.xticks(fontsize=16, fontstyle='italic')
    plt.ylabel(ylabels, fontweight='bold', fontsize=20)
    plt.yticks(fontsize=16, fontstyle='italic')
    plt.title(title, fontweight= 'bold', fontstyle='italic', fontsize=24)
    plt.grid(color='white')


def plot_cumulative_gains(actual, prob_pred, return_plot_table=False):
    '''Builds a cumulative gains curve and compares it that of random 
        and optimal model curves'''

    # Init in a dataframe to simplify some operations
    temp = pd.DataFrame(list(zip(actual, prob_pred)), columns=['actual', 'pred'])
    temp = temp.sort_values(by='pred', ascending=False)
    temp['rank'] = np.array(range(len(temp))) +1
    
    # Create optimal column which pushes positives to the top of the ranked list
    temp['optimal'] = 0
    temp.loc[temp['rank']<sum(actual)+1, 'optimal'] = 1

    # Add cumulative sum columns for 
    temp['cumsum_pred'] = temp['actual'].cumsum()
    temp['cumsum_optimal'] = temp['optimal'].cumsum()

    # Calculate AUC ratio (predictions/optimal)
    auc_optimal = auc(temp['rank'].values, temp['cumsum_optimal'].values)
    auc_pred = auc(temp['rank'].values, temp['cumsum_pred'].values)
    error_rate = round(1-(auc_pred/auc_optimal),3)
    print('Error rate (1 - (AUC pred / AUC optimal)): ', error_rate)

    plt.subplots(1,1, figsize=[10, 6], facecolor='white')
    plt.style.use('fivethirtyeight')
    plt.plot([1,len(actual)],[0, sum(actual)], 'k--')
    plt.plot(temp['rank'].values, temp['cumsum_optimal'])
    plt.plot(temp['rank'].values, temp['cumsum_pred'])

    plt.xlabel('Rank', fontweight='bold', fontsize=20)
    plt.ylabel('Cumulative Total', fontweight='bold', fontsize=20)
    plt.title('Cumulative Gains of Prediction Model', fontweight= 'bold', fontstyle='italic', fontsize=24)
    plt.xticks(fontsize=16, fontstyle='italic')
    plt.yticks(fontsize=16, fontstyle='italic')
    plt.legend(['Random', 'Optimal', 'Predicted'])
    
    if return_plot_table:
        return temp
