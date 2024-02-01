import axios from "axios";
import * as cheerio from "cheerio";


function get_card_list(): void {
    let base_url = 'https://cardfight.fandom.com';
    let initial_url = base_url + '/wiki/Category:Cards';
    let card_list = [];
    let forbidden_keywords = [
        'Category:', 
        'Gallery:', 
        'Trivia:', 
        'Errata:', 
        'Tips:', 
        'Rulings:', 
        'Lores:', 
        '(ZERO)', 
        'User:', 
        '_Gallery', 
        'User_blog:'
    ];


}   
