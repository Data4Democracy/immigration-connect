import numpy as np
import matplotlib.pyplot as plt

# There are about 689800 Dreamers whose DACA status was current as of Sept. 4, 2017 - 
# each point plotted will represent rec_per_point of them
num_rec = 689800
rec_per_point = 100

# Interactively parsed http://bit.ly/2AZKXl0 to get numbers of individuals with 
# pending renewals or denied/expiring DACA status for each month Sept. 2017-Sept. 2019
# Numbers for Oct. 2019-Mar. 2020 were calculated according to the 2 year expiration 
# from the last approved renewal date
exp_month=['September 2017','October 2017','November 2017','December 2017',
           'January 2018','February 2018','March 2018','April 2018','May 2018',
           'June 2018','July 2018','August 2018','September 2018','October 2018',
           'November 2018','December 2018','January 2019','February 2019','March 2019',
           'April 2019','May 2019','June 2019','July 2019','August 2019',
           'September 2019','October 2019','November 2019','December 2019',
           'January 2020','February 2020','March 2020']
imfile=['201709','201710','201711','201712','201801','201802','201803','201804',
        '201805','201806','201807','201808','201809','201810','201811','201812',
        '201901','201902','201903','201904','201905','201906','201907','201908',
        '201909','201910','201911','201912','202001','202002','202003']
undoc=np.array([1830,4030,5980,12500,18730,21820,34960,40330,54330,63440,67310,103390,
                136970,181060,208550,228800,278130,326440,378160,415410,447680,483900,
                516250,557040,565530,577920,591040,637310,674090,688790,689350])
pending_acc=np.array([2590,6910,11370,27600,43640,51610,51960,51970,51990,52000,52000,
                      52010,52020,52030,52040,52050,52060,52070,52070,52070,52080,
                      52090,52100,52110,49520,45200,40740,24510,8470,500,150])

# Only plot 1/rec_per_point points instead of all ~700k to make each point easier to see
num_rec = num_rec//rec_per_point
undoc=np.round(undoc/rec_per_point)
pending=np.round(pending_acc/rec_per_point)

# Set up uniform distribution of points to plot
xval = np.random.uniform(0,1,num_rec)
yval = np.random.uniform(0,0.8,num_rec)


for i,u in enumerate(undoc):
#    plt.figure(figsize=(8, 6), dpi= 80, facecolor=[0.5,0.5,0.5], edgecolor='k')
    plt.figure(facecolor=[0.5,0.5,0.5], edgecolor='k')

    # plot grey x's for Dreamers who become undocumented
    plt.scatter(xval[0:u], yval[0:u], s=10, marker='x', c=[0.4,0.4,0.4], edgecolors='none',
                label='Undocumented former DACA recipients')

    # plot green diamonds for Dreamers with current DACA status
    plt.scatter(xval[u+pending[i]:num_rec], yval[u+pending[i]:num_rec], s=10, marker='d', 
                c=[0,1,0], edgecolors='none', label='Active DACA recipients')

    # plot yellow diamonds for Dreamers with a pending renewal request
    plt.scatter(xval[u:u+pending[i]], yval[u:u+pending[i]], s=10, marker='d', c=[0.8,1,0], 
                edgecolors='none', label='DACA recipients pending renewal as of Sept. 4, 2017')

    plt.text(0.05,-0.05,exp_month[i], color='white', weight='bold')
#    plt.legend()
    plt.axis('off')
#    plt.show()
    plt.savefig(imfile[i] + '.png', facecolor=[0.5,0.5,0.5], dpi=120)
    plt.close()

# Used Gimp to crop and make .gif from .pngs
