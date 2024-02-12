"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.get_card_dict = void 0;
var cheerio = require("cheerio");
var BASE_URL = 'https://cardfight.fandom.com/wiki/';
// interface data {
//     [key: string]: string | number | string[] | Record<string, string>;
// }
// const get_main_info = async ($: cheerio.CheerioAPI, page: string) => {
//     const mainInfo: data = {};
//     const $info_main = $('.info-main').children('td');
//     for (let i = 0; i < $info_main.length; i +=2) {
//     }
//     return mainInfo;
// }
// const get_sets = async (card: string) => {
// }
// const get_flavor_text = async (card: string) => {
// }
// const get_effects = async (card: string) => {
// }
// const get_tourney_status = async (card: string) => {
// }
var get_card_dict = function (card) {
    var page = BASE_URL + card;
    //const response = await axios.get(page);
    var $ = cheerio.load(page);
    //let data = get_main_info($, page);
    // data['Sets'] = get_sets($);
    console.log($);
};
exports.get_card_dict = get_card_dict;
(0, exports.get_card_dict)('Sheltered_Heiress,_Spangled');
