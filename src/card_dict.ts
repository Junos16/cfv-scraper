import axios from 'axios';
import * as cheerio from 'cheerio';

const BASE_URL = 'https://cardfight.fandom.com/wiki/';

interface data {
    [key: string]: null | string | number | string[] | Record<string, string> | data;
}

const getMainInfo = async ($: cheerio.CheerioAPI, card: string): Promise<data> => {
    let main_info: data = {};
    const $info_main = $('.info-main tr');

    $info_main.each(function () {
        const key = $(this).find('td').eq(0).text().replace('\n', '');
        const value = $(this).find('td').eq(1).text().replace('\n', '');
        
        if (key.includes('Grade')) {
            const keys = key.split('/', 2).map(str => str.trim());
            if (value.includes('/')) {
                const values = value.split('/').map(str => str.trim());
                const value0 = parseInt(values[0].split(' ')[1], 10); 
                const value1 = values.slice(1); 
                main_info[keys[0]] = value0;
                main_info[keys[1]] = value1.length > 1 ? value1: value1[0];
            } else {
                main_info[keys[0]] = parseInt(value.split(' ')[1], 10); 
                main_info[keys[1]] = null;
            }
        }

        else if (['Power', 'Shield', 'Critical'].includes(key)) {
            if (!['N/A', 'None'].includes(value)) {
                const new_value = parseInt(value.replace('+', '').replace(',', ''), 10);
                main_info[key] = new_value;
            } else main_info[key] = null;
        }

        else if (key == 'Imaginary Gift') {
            const new_key = 'Ride';
            let new_value;
            try {
                new_value = $(this).find('td').eq(1).find('a title');
            } finally {
                new_value = null;
            }
            main_info[new_key] = new_value;
        }
        
        else main_info[key] = value;
    });

    if (main_info['Format'] != 'Premium') {
        const new_value = main_info['Format']?.toString().includes('Standard') ? 'D ' : 'V ';
        main_info['Format'] = new_value + main_info['Format'];
        main_info['Format'] = main_info['Format'].split('/').map(str => str.trim());
    }

    main_info['Link'] = BASE_URL + card.replace(/\s+/g, '_');

    return main_info;
}

const getExtraInfo = async (info: data, card: string) => {
    const export_page = BASE_URL + 'Special:Export/' + card.replace(/\s+/g, '_');
    const $txt = await getHtml(export_page);

    if ($txt('text').text().includes('Persona')) info['Ride'] = 'Persona';

    info['ID'] = $txt('page id').text();
    info['Title'] = $txt('page title').text();
}

const getSets = async ($: cheerio.CheerioAPI): Promise<data> => {
    let sets: data = {};
    const $sets = $('.sets li');

    $sets.each(function() {
        $(this).find('br').replaceWith(' - ');
        const set_list = $(this).text().trim().split(' - ');
        const key = set_list[0];
        const value = set_list.splice(1);
        sets[key] = value;
    })

    return sets;
}

const getFlavorText = async ($: cheerio.CheerioAPI): Promise<data | string> => {
    const $flavor = $('.flavor td');
    const flavor_text = $flavor.text().trim();
    if (flavor_text.includes(':')) {
        const flavor_list = flavor_text.split(/\s(?=\([^)]+\):)/);
        const flavors: data = {};
        flavor_list.forEach(ele => {
            const parts = ele.split(':');
            const key = parts[0].trim();
            const value = parts.slice(1).join(':').trim();
            flavors[key] = value;
        }) 
        return flavors;
    } else return flavor_text;
}

const parseEffect = async ($: cheerio.Cheerio<cheerio.Element>): Promise<string []> => {
    $.find('br').replaceWith('|||');
    const effect_text = $.text();
    const effect_list = effect_text.split('|||');
    return effect_list;
}

// Fix pages with tabber
const getEffects = async ($: cheerio.CheerioAPI): Promise<string[] | data> => {
    //const effects: data = {};
    const $effects = $('.effect td');
    const $tabber = $('.effect div.tabber wds-tabber');

    if ($tabber) {
        const effects: data = {};
        // const keys: string[] = [];
        // const values: any = [];

        // $tabber.find('a').each(function() {
        //     const key = $(this).text();
        //     keys.push(key);
        // });

        // console.log(keys);
        
        // const value_tags = $tabber.find('.wds-tab__content wds-is-current').nextAll('div');
        // value_tags.each(function() {
        //     $(this).find('br').replaceWith('|||');
        //     const value_text = $(this).text();
        //     const value_list = value_text.split('|||');
        //     values.push(value_list);
        // });

        // keys.forEach((key, index) => {
        //     effects[key] = values[index];
        // });
        
        return effects;
    } else return await parseEffect($effects);
}

// Fix pages with restricted icons in tourney status
const getTourneyStatus = async ($: cheerio.CheerioAPI): Promise<data> => {
    const $tourney_status = $('.tourneystatus tr');
    const tourney_status: data = {};

    $tourney_status.slice(1).each(function() {
        const key = $(this).find('td').eq(0).text().trim();
        const value = $(this).find('td').eq(1).text().trim();
        tourney_status[key] = value;
    })

    return tourney_status;
}

const getHtml = async (page: string): Promise<cheerio.CheerioAPI> => {
    const response = await axios.get(page);
    const $ = cheerio.load(response.data);
    return $;
}

const getCardData = async (card: string): Promise<data> => {
    const page = BASE_URL + card.replace(/\s+/g, '_');
    const $ = await getHtml(page);
    
    let card_data: data = await getMainInfo($, card);
    await getExtraInfo(card_data, card);
    
    card_data['Sets'] = await getSets($);
    card_data['Flavors'] = await getFlavorText($);
    card_data['Effects'] = await getEffects($);
    card_data['Tourney Status'] = await getTourneyStatus($);

    return card_data;
}

getCardData('Vampire Princess of Starlight, Nightrose').then((card_data) => { 
    console.log(card_data)
}).catch(error => {
    console.error('Error', error.message);
});