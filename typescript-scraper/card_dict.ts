import axios from "axios";
import * as cheerio from "cheerio";

function get_main_info() {

}

function get_sets() {

}

function get_flavor_text() {

}

function get_effects() {

}

function get_tourney_status() {

}

async function get_card_dict(card: string) {
    let base_url = 'https://cardfight.fandom.com/wiki/';
    let page = base_url + card;
    const response = await axios.get(page);
    const $ = cheerio.load(response.data);

    const $info_main = $('.info-main td');
    let data = get_main_info($info_main);

    try {
        const $sets = $('sets li');
    } catch(error) {
        console.error();
    }

    try {
        const $flavor = $('flavor li')
    } catch(error) {

    }

    try {

    } catch(error) {

    }
}