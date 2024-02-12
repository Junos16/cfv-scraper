import axios from "axios";
import * as cheerio from "cheerio";

const get_main_info = async (card: cheerio.Cheerio<cheerio.Element>) {

}

const get_sets = async (card: string) {

}

const get_flavor_text = async (card: string) {

}

const get_effects = async (card: string) {

}

const get_tourney_status = async (card: string) {

}

export const get_card_dict  = async (card: string) => {
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