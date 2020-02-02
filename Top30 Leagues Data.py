import data_scrapper as ds
import requests
from bs4 import BeautifulSoup
import bs4
import itertools
import time
import tqdm
import os
import sys

def standings_updater():
    #Update Standings - By league and all leagues together
    standings = ds.league_link_standings().get_links_standings()
    print('\n')
    print("Saving all the leagues' standings")
    pbar = tqdm.tqdm(range(len(standings.keys())))
    for i, league, link in zip(pbar, standings.keys(), list(standings.values())):
        ds.dataframe_to_excel(ds.league_table_dataframe(league, link).get_standings(), 'Standings').save_dataframe()
        pbar.set_description(" Updating {}'s standings".format(league))
        time.sleep(0.1)
    print("All the leagues' standings has been saved")
    print('\n')
    print('Saving all the standings together')
    ds.dataframe_to_excel(ds.all_dataframes_together(standings, 'Standings').mod_dataframe(),'Standings').save_dataframe()
    
def players_updater(all_scr_asst_gkpr):
    #Update Scorers, Assistants and Goalkeepers - By league and all together
    players = ds.league_link_players().get_links_players()
    if all_scr_asst_gkpr == 'Update all':
        iterator = ['Scorers', 'Assistants', 'Goalkeepers']
    else:
        iterator = [all_scr_asst_gkpr]
    for iteration in iterator:
        print('\n')
        print('Saving the {}'.format(iteration))
        pbar = tqdm.tqdm(range(len(players.keys())))
        for i, league, link in zip(pbar, players.keys(), list(players.values())):
            ds.dataframe_to_excel(ds.scorer_assist_gkeepr_df(league, link, iteration).get_ranking(),iteration).save_dataframe()
            pbar.set_description(" Updating {}'s {}".format(league, iteration.lower()))
            time.sleep(0.1)
        print("All the leagues' {} has been saved".format(iteration.lower()))
        print('\n')
        print('Saving all the {} together'.format(iteration.lower()))
        ds.dataframe_to_excel(ds.all_dataframes_together(players, iteration).mod_dataframe(),iteration).save_dataframe()

def choicer():
    user_choice = str(input("\nWhat would you like to do?\n\n- Update all the data (Update all)\n\n- Update specific data (Update specific)\n\n"))
    if user_choice == 'Update all':
        standings_updater()
        players_updater(user_choice)
        print("The data has been saved in {}/{}".format(os.getcwd(),'Saved dataframes'))
    if user_choice == 'Update specific':
        choice_2 = str(input("\nWhat would you like to update (Standings / Scorers / Assistants / Goalkeepers): "))
        if choice_2 == 'Standings':
            standings_updater()
        else:
            players_updater(choice_2)
        out_path = '{}/{}/{}'.format(os.getcwd(),'Saved dataframes',choice_2)
        print("The data has been saved in {}".format(out_path))
    re_choice = str(input('Would you like to do anything else or exit the program (Anything else / Exit): '))
    if re_choice == 'Anything else':
        choicer()
    if re_choice == 'Exit':
        exit()

print("\nWelcome to the 'Top30 Football Leagues Data Downloader'\n\nWith this program you will be able to download updated data of the Standings, Top Scorers, Top Assistants and Top Goalkeepers from the 30 most important football leagues in the world. Let's start!")
choicer()