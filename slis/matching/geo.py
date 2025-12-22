from typing import Dict, Any, List


COUNTRY_DATA = [
    { 'code': 'AF', 'code3': 'AFG', 'nameEn': 'Afghanistan', 'nameId': 'Afganistan' },
    { 'code': 'AL', 'code3': 'ALB', 'nameEn': 'Albania', 'nameId': 'Albania' },
    { 'code': 'DZ', 'code3': 'DZA', 'nameEn': 'Algeria', 'nameId': 'Aljazair' },
    { 'code': 'AD', 'code3': 'AND', 'nameEn': 'Andorra', 'nameId': 'Andorra' },
    { 'code': 'AO', 'code3': 'AGO', 'nameEn': 'Angola', 'nameId': 'Angola' },
    { 'code': 'AG', 'code3': 'ATG', 'nameEn': 'Antigua and Barbuda', 'nameId': 'Antigua dan Barbuda' },
    { 'code': 'AR', 'code3': 'ARG', 'nameEn': 'Argentina', 'nameId': 'Argentina' },
    { 'code': 'AM', 'code3': 'ARM', 'nameEn': 'Armenia', 'nameId': 'Armenia' },
    { 'code': 'AU', 'code3': 'AUS', 'nameEn': 'Australia', 'nameId': 'Australia' },
    { 'code': 'AT', 'code3': 'AUT', 'nameEn': 'Austria', 'nameId': 'Austria' },
    { 'code': 'AZ', 'code3': 'AZE', 'nameEn': 'Azerbaijan', 'nameId': 'Azerbaijan' },
    { 'code': 'BS', 'code3': 'BHS', 'nameEn': 'Bahamas', 'nameId': 'Bahama' },
    { 'code': 'BH', 'code3': 'BHR', 'nameEn': 'Bahrain', 'nameId': 'Bahrain' },
    { 'code': 'BD', 'code3': 'BGD', 'nameEn': 'Bangladesh', 'nameId': 'Bangladesh' },
    { 'code': 'BB', 'code3': 'BRB', 'nameEn': 'Barbados', 'nameId': 'Barbados' },
    { 'code': 'BY', 'code3': 'BLR', 'nameEn': 'Belarus', 'nameId': 'Belarus' },
    { 'code': 'BE', 'code3': 'BEL', 'nameEn': 'Belgium', 'nameId': 'Belgia' },
    { 'code': 'BZ', 'code3': 'BLZ', 'nameEn': 'Belize', 'nameId': 'Belize' },
    { 'code': 'BJ', 'code3': 'BEN', 'nameEn': 'Benin', 'nameId': 'Benin' },
    { 'code': 'BT', 'code3': 'BTN', 'nameEn': 'Bhutan', 'nameId': 'Bhutan' },
    { 'code': 'BO', 'code3': 'BOL', 'nameEn': 'Bolivia', 'nameId': 'Bolivia' },
    { 'code': 'BA', 'code3': 'BIH', 'nameEn': 'Bosnia and Herzegovina', 'nameId': 'Bosnia dan Herzegovina' },
    { 'code': 'BW', 'code3': 'BWA', 'nameEn': 'Botswana', 'nameId': 'Botswana' },
    { 'code': 'BR', 'code3': 'BRA', 'nameEn': 'Brazil', 'nameId': 'Brasil' },
    { 'code': 'BN', 'code3': 'BRN', 'nameEn': 'Brunei', 'nameId': 'Brunei' },
    { 'code': 'BG', 'code3': 'BGR', 'nameEn': 'Bulgaria', 'nameId': 'Bulgaria' },
    { 'code': 'BF', 'code3': 'BFA', 'nameEn': 'Burkina Faso', 'nameId': 'Burkina Faso' },
    { 'code': 'BI', 'code3': 'BDI', 'nameEn': 'Burundi', 'nameId': 'Burundi' },
    { 'code': 'CV', 'code3': 'CPV', 'nameEn': 'Cabo Verde', 'nameId': 'Tanjung Verde' },
    { 'code': 'KH', 'code3': 'KHM', 'nameEn': 'Cambodia', 'nameId': 'Kamboja' },
    { 'code': 'CM', 'code3': 'CMR', 'nameEn': 'Cameroon', 'nameId': 'Kamerun' },
    { 'code': 'CA', 'code3': 'CAN', 'nameEn': 'Canada', 'nameId': 'Kanada' },
    { 'code': 'CF', 'code3': 'CAF', 'nameEn': 'Central African Republic', 'nameId': 'Republik Afrika Tengah' },
    { 'code': 'TD', 'code3': 'TCD', 'nameEn': 'Chad', 'nameId': 'Chad' },
    { 'code': 'CL', 'code3': 'CHL', 'nameEn': 'Chile', 'nameId': 'Chili' },
    { 'code': 'CN', 'code3': 'CHN', 'nameEn': 'China', 'nameId': 'Tiongkok' },
    { 'code': 'CO', 'code3': 'COL', 'nameEn': 'Colombia', 'nameId': 'Kolombia' },
    { 'code': 'KM', 'code3': 'COM', 'nameEn': 'Comoros', 'nameId': 'Komoro' },
    { 'code': 'CD', 'code3': 'COD', 'nameEn': 'Congo (Democratic Republic)', 'nameId': 'Kongo (Republik Demokratik)' },
    { 'code': 'CG', 'code3': 'COG', 'nameEn': 'Congo (Republic)', 'nameId': 'Kongo (Republik)' },
    { 'code': 'CR', 'code3': 'CRI', 'nameEn': 'Costa Rica', 'nameId': 'Kosta Rika' },
    { 'code': 'CI', 'code3': 'CIV', 'nameEn': "Cote d'Ivoire", 'nameId': 'Pantai Gading' },
    { 'code': 'HR', 'code3': 'HRV', 'nameEn': 'Croatia', 'nameId': 'Kroasia' },
    { 'code': 'CU', 'code3': 'CUB', 'nameEn': 'Cuba', 'nameId': 'Kuba' },
    { 'code': 'CY', 'code3': 'CYP', 'nameEn': 'Cyprus', 'nameId': 'Siprus' },
    { 'code': 'CZ', 'code3': 'CZE', 'nameEn': 'Czech Republic', 'nameId': 'Republik Ceko' },
    { 'code': 'DK', 'code3': 'DNK', 'nameEn': 'Denmark', 'nameId': 'Denmark' },
    { 'code': 'DJ', 'code3': 'DJI', 'nameEn': 'Djibouti', 'nameId': 'Djibouti' },
    { 'code': 'DM', 'code3': 'DMA', 'nameEn': 'Dominica', 'nameId': 'Dominika' },
    { 'code': 'DO', 'code3': 'DOM', 'nameEn': 'Dominican Republic', 'nameId': 'Republik Dominika' },
    { 'code': 'EC', 'code3': 'ECU', 'nameEn': 'Ecuador', 'nameId': 'Ekuador' },
    { 'code': 'EG', 'code3': 'EGY', 'nameEn': 'Egypt', 'nameId': 'Mesir' },
    { 'code': 'SV', 'code3': 'SLV', 'nameEn': 'El Salvador', 'nameId': 'El Salvador' },
    { 'code': 'GQ', 'code3': 'GNQ', 'nameEn': 'Equatorial Guinea', 'nameId': 'Guinea Khatulistiwa' },
    { 'code': 'ER', 'code3': 'ERI', 'nameEn': 'Eritrea', 'nameId': 'Eritrea' },
    { 'code': 'EE', 'code3': 'EST', 'nameEn': 'Estonia', 'nameId': 'Estonia' },
    { 'code': 'SZ', 'code3': 'SWZ', 'nameEn': 'Eswatini', 'nameId': 'Eswatini' },
    { 'code': 'ET', 'code3': 'ETH', 'nameEn': 'Ethiopia', 'nameId': 'Ethiopia' },
    { 'code': 'FJ', 'code3': 'FJI', 'nameEn': 'Fiji', 'nameId': 'Fiji' },
    { 'code': 'FI', 'code3': 'FIN', 'nameEn': 'Finland', 'nameId': 'Finlandia' },
    { 'code': 'FR', 'code3': 'FRA', 'nameEn': 'France', 'nameId': 'Prancis' },
    { 'code': 'GA', 'code3': 'GAB', 'nameEn': 'Gabon', 'nameId': 'Gabon' },
    { 'code': 'GM', 'code3': 'GMB', 'nameEn': 'Gambia', 'nameId': 'Gambia' },
    { 'code': 'GE', 'code3': 'GEO', 'nameEn': 'Georgia', 'nameId': 'Georgia' },
    { 'code': 'DE', 'code3': 'DEU', 'nameEn': 'Germany', 'nameId': 'Jerman' },
    { 'code': 'GH', 'code3': 'GHA', 'nameEn': 'Ghana', 'nameId': 'Ghana' },
    { 'code': 'GR', 'code3': 'GRC', 'nameEn': 'Greece', 'nameId': 'Yunani' },
    { 'code': 'GD', 'code3': 'GRD', 'nameEn': 'Grenada', 'nameId': 'Grenada' },
    { 'code': 'GT', 'code3': 'GTM', 'nameEn': 'Guatemala', 'nameId': 'Guatemala' },
    { 'code': 'GN', 'code3': 'GIN', 'nameEn': 'Guinea', 'nameId': 'Guinea' },
    { 'code': 'GW', 'code3': 'GNB', 'nameEn': 'Guinea-Bissau', 'nameId': 'Guinea-Bissau' },
    { 'code': 'GY', 'code3': 'GUY', 'nameEn': 'Guyana', 'nameId': 'Guyana' },
    { 'code': 'HT', 'code3': 'HTI', 'nameEn': 'Haiti', 'nameId': 'Haiti' },
    { 'code': 'HN', 'code3': 'HND', 'nameEn': 'Honduras', 'nameId': 'Honduras' },
    { 'code': 'HU', 'code3': 'HUN', 'nameEn': 'Hungary', 'nameId': 'Hungaria' },
    { 'code': 'IS', 'code3': 'ISL', 'nameEn': 'Iceland', 'nameId': 'Islandia' },
    { 'code': 'IN', 'code3': 'IND', 'nameEn': 'India', 'nameId': 'India' },
    { 'code': 'ID', 'code3': 'IDN', 'nameEn': 'Indonesia', 'nameId': 'Indonesia' },
    { 'code': 'IR', 'code3': 'IRN', 'nameEn': 'Iran', 'nameId': 'Iran' },
    { 'code': 'IQ', 'code3': 'IRQ', 'nameEn': 'Iraq', 'nameId': 'Irak' },
    { 'code': 'IE', 'code3': 'IRL', 'nameEn': 'Ireland', 'nameId': 'Irlandia' },
    { 'code': 'IL', 'code3': 'ISR', 'nameEn': 'Israel', 'nameId': 'Israel' },
    { 'code': 'IT', 'code3': 'ITA', 'nameEn': 'Italy', 'nameId': 'Italia' },
    { 'code': 'JM', 'code3': 'JAM', 'nameEn': 'Jamaica', 'nameId': 'Jamaika' },
    { 'code': 'JP', 'code3': 'JPN', 'nameEn': 'Japan', 'nameId': 'Jepang' },
    { 'code': 'JO', 'code3': 'JOR', 'nameEn': 'Jordan', 'nameId': 'Yordania' },
    { 'code': 'KZ', 'code3': 'KAZ', 'nameEn': 'Kazakhstan', 'nameId': 'Kazakhstan' },
    { 'code': 'KE', 'code3': 'KEN', 'nameEn': 'Kenya', 'nameId': 'Kenya' },
    { 'code': 'KI', 'code3': 'KIR', 'nameEn': 'Kiribati', 'nameId': 'Kiribati' },
    { 'code': 'KW', 'code3': 'KWT', 'nameEn': 'Kuwait', 'nameId': 'Kuwait' },
    { 'code': 'KG', 'code3': 'KGZ', 'nameEn': 'Kyrgyzstan', 'nameId': 'Kirgizstan' },
    { 'code': 'LA', 'code3': 'LAO', 'nameEn': 'Laos', 'nameId': 'Laos' },
    { 'code': 'LV', 'code3': 'LVA', 'nameEn': 'Latvia', 'nameId': 'Latvia' },
    { 'code': 'LB', 'code3': 'LBN', 'nameEn': 'Lebanon', 'nameId': 'Lebanon' },
    { 'code': 'LS', 'code3': 'LSO', 'nameEn': 'Lesotho', 'nameId': 'Lesotho' },
    { 'code': 'LR', 'code3': 'LBR', 'nameEn': 'Liberia', 'nameId': 'Liberia' },
    { 'code': 'LY', 'code3': 'LBY', 'nameEn': 'Libya', 'nameId': 'Libya' },
    { 'code': 'LI', 'code3': 'LIE', 'nameEn': 'Liechtenstein', 'nameId': 'Liechtenstein' },
    { 'code': 'LT', 'code3': 'LTU', 'nameEn': 'Lithuania', 'nameId': 'Lithuania' },
    { 'code': 'LU', 'code3': 'LUX', 'nameEn': 'Luxembourg', 'nameId': 'Luksemburg' },
    { 'code': 'MG', 'code3': 'MDG', 'nameEn': 'Madagascar', 'nameId': 'Madagaskar' },
    { 'code': 'MW', 'code3': 'MWI', 'nameEn': 'Malawi', 'nameId': 'Malawi' },
    { 'code': 'MY', 'code3': 'MYS', 'nameEn': 'Malaysia', 'nameId': 'Malaysia' },
    { 'code': 'MV', 'code3': 'MDV', 'nameEn': 'Maldives', 'nameId': 'Maladewa' },
    { 'code': 'ML', 'code3': 'MLI', 'nameEn': 'Mali', 'nameId': 'Mali' },
    { 'code': 'MT', 'code3': 'MLT', 'nameEn': 'Malta', 'nameId': 'Malta' },
    { 'code': 'MH', 'code3': 'MHL', 'nameEn': 'Marshall Islands', 'nameId': 'Kepulauan Marshall' },
    { 'code': 'MR', 'code3': 'MRT', 'nameEn': 'Mauritania', 'nameId': 'Mauritania' },
    { 'code': 'MU', 'code3': 'MUS', 'nameEn': 'Mauritius', 'nameId': 'Mauritius' },
    { 'code': 'MX', 'code3': 'MEX', 'nameEn': 'Mexico', 'nameId': 'Meksiko' },
    { 'code': 'FM', 'code3': 'FSM', 'nameEn': 'Micronesia', 'nameId': 'Mikronesia' },
    { 'code': 'MD', 'code3': 'MDA', 'nameEn': 'Moldova', 'nameId': 'Moldova' },
    { 'code': 'MC', 'code3': 'MCO', 'nameEn': 'Monaco', 'nameId': 'Monako' },
    { 'code': 'MN', 'code3': 'MNG', 'nameEn': 'Mongolia', 'nameId': 'Mongolia' },
    { 'code': 'ME', 'code3': 'MNE', 'nameEn': 'Montenegro', 'nameId': 'Montenegro' },
    { 'code': 'MA', 'code3': 'MAR', 'nameEn': 'Morocco', 'nameId': 'Maroko' },
    { 'code': 'MZ', 'code3': 'MOZ', 'nameEn': 'Mozambique', 'nameId': 'Mozambik' },
    { 'code': 'MM', 'code3': 'MMR', 'nameEn': 'Myanmar', 'nameId': 'Myanmar' },
    { 'code': 'NA', 'code3': 'NAM', 'nameEn': 'Namibia', 'nameId': 'Namibia' },
    { 'code': 'NR', 'code3': 'NRU', 'nameEn': 'Nauru', 'nameId': 'Nauru' },
    { 'code': 'NP', 'code3': 'NPL', 'nameEn': 'Nepal', 'nameId': 'Nepal' },
    { 'code': 'NL', 'code3': 'NLD', 'nameEn': 'Netherlands', 'nameId': 'Belanda' },
    { 'code': 'NZ', 'code3': 'NZL', 'nameEn': 'New Zealand', 'nameId': 'Selandia Baru' },
    { 'code': 'NI', 'code3': 'NIC', 'nameEn': 'Nicaragua', 'nameId': 'Nikaragua' },
    { 'code': 'NE', 'code3': 'NER', 'nameEn': 'Niger', 'nameId': 'Niger' },
    { 'code': 'NG', 'code3': 'NGA', 'nameEn': 'Nigeria', 'nameId': 'Nigeria' },
    { 'code': 'KP', 'code3': 'PRK', 'nameEn': 'North Korea', 'nameId': 'Korea Utara' },
    { 'code': 'MK', 'code3': 'MKD', 'nameEn': 'North Macedonia', 'nameId': 'Makedonia Utara' },
    { 'code': 'NO', 'code3': 'NOR', 'nameEn': 'Norway', 'nameId': 'Norwegia' },
    { 'code': 'OM', 'code3': 'OMN', 'nameEn': 'Oman', 'nameId': 'Oman' },
    { 'code': 'PK', 'code3': 'PAK', 'nameEn': 'Pakistan', 'nameId': 'Pakistan' },
    { 'code': 'PW', 'code3': 'PLW', 'nameEn': 'Palau', 'nameId': 'Palau' },
    { 'code': 'PS', 'code3': 'PSE', 'nameEn': 'Palestine', 'nameId': 'Palestina' },
    { 'code': 'PA', 'code3': 'PAN', 'nameEn': 'Panama', 'nameId': 'Panama' },
    { 'code': 'PG', 'code3': 'PNG', 'nameEn': 'Papua New Guinea', 'nameId': 'Papua Nugini' },
    { 'code': 'PY', 'code3': 'PRY', 'nameEn': 'Paraguay', 'nameId': 'Paraguay' },
    { 'code': 'PE', 'code3': 'PER', 'nameEn': 'Peru', 'nameId': 'Peru' },
    { 'code': 'PH', 'code3': 'PHL', 'nameEn': 'Philippines', 'nameId': 'Filipina' },
    { 'code': 'PL', 'code3': 'POL', 'nameEn': 'Poland', 'nameId': 'Polandia' },
    { 'code': 'PT', 'code3': 'PRT', 'nameEn': 'Portugal', 'nameId': 'Portugal' },
    { 'code': 'QA', 'code3': 'QAT', 'nameEn': 'Qatar', 'nameId': 'Qatar' },
    { 'code': 'RO', 'code3': 'ROU', 'nameEn': 'Romania', 'nameId': 'Rumania' },
    { 'code': 'RU', 'code3': 'RUS', 'nameEn': 'Russia', 'nameId': 'Rusia' },
    { 'code': 'RW', 'code3': 'RWA', 'nameEn': 'Rwanda', 'nameId': 'Rwanda' },
    { 'code': 'KN', 'code3': 'KNA', 'nameEn': 'Saint Kitts and Nevis', 'nameId': 'Saint Kitts dan Nevis' },
    { 'code': 'LC', 'code3': 'LCA', 'nameEn': 'Saint Lucia', 'nameId': 'Saint Lucia' },
    { 'code': 'VC', 'code3': 'VCT', 'nameEn': 'Saint Vincent and the Grenadines', 'nameId': 'Saint Vincent dan Grenadines' },
    { 'code': 'WS', 'code3': 'WSM', 'nameEn': 'Samoa', 'nameId': 'Samoa' },
    { 'code': 'SM', 'code3': 'SMR', 'nameEn': 'San Marino', 'nameId': 'San Marino' },
    { 'code': 'ST', 'code3': 'STP', 'nameEn': 'Sao Tome and Principe', 'nameId': 'Sao Tome dan Principe' },
    { 'code': 'SA', 'code3': 'SAU', 'nameEn': 'Saudi Arabia', 'nameId': 'Arab Saudi' },
    { 'code': 'SN', 'code3': 'SEN', 'nameEn': 'Senegal', 'nameId': 'Senegal' },
    { 'code': 'RS', 'code3': 'SRB', 'nameEn': 'Serbia', 'nameId': 'Serbia' },
    { 'code': 'SC', 'code3': 'SYC', 'nameEn': 'Seychelles', 'nameId': 'Seychelles' },
    { 'code': 'SL', 'code3': 'SLE', 'nameEn': 'Sierra Leone', 'nameId': 'Sierra Leone' },
    { 'code': 'SG', 'code3': 'SGP', 'nameEn': 'Singapore', 'nameId': 'Singapura' },
    { 'code': 'SK', 'code3': 'SVK', 'nameEn': 'Slovakia', 'nameId': 'Slovakia' },
    { 'code': 'SI', 'code3': 'SVN', 'nameEn': 'Slovenia', 'nameId': 'Slovenia' },
    { 'code': 'SB', 'code3': 'SLB', 'nameEn': 'Solomon Islands', 'nameId': 'Kepulauan Solomon' },
    { 'code': 'SO', 'code3': 'SOM', 'nameEn': 'Somalia', 'nameId': 'Somalia' },
    { 'code': 'ZA', 'code3': 'ZAF', 'nameEn': 'South Africa', 'nameId': 'Afrika Selatan' },
    { 'code': 'KR', 'code3': 'KOR', 'nameEn': 'South Korea', 'nameId': 'Korea Selatan' },
    { 'code': 'SS', 'code3': 'SSD', 'nameEn': 'South Sudan', 'nameId': 'Sudan Selatan' },
    { 'code': 'ES', 'code3': 'ESP', 'nameEn': 'Spain', 'nameId': 'Spanyol' },
    { 'code': 'LK', 'code3': 'LKA', 'nameEn': 'Sri Lanka', 'nameId': 'Sri Lanka' },
    { 'code': 'SD', 'code3': 'SDN', 'nameEn': 'Sudan', 'nameId': 'Sudan' },
    { 'code': 'SR', 'code3': 'SUR', 'nameEn': 'Suriname', 'nameId': 'Suriname' },
    { 'code': 'SE', 'code3': 'SWE', 'nameEn': 'Sweden', 'nameId': 'Swedia' },
    { 'code': 'CH', 'code3': 'CHE', 'nameEn': 'Switzerland', 'nameId': 'Swiss' },
    { 'code': 'SY', 'code3': 'SYR', 'nameEn': 'Syria', 'nameId': 'Suriah' },
    { 'code': 'TW', 'code3': 'TWN', 'nameEn': 'Taiwan', 'nameId': 'Taiwan' },
    { 'code': 'TJ', 'code3': 'TJK', 'nameEn': 'Tajikistan', 'nameId': 'Tajikistan' },
    { 'code': 'TZ', 'code3': 'TZA', 'nameEn': 'Tanzania', 'nameId': 'Tanzania' },
    { 'code': 'TH', 'code3': 'THA', 'nameEn': 'Thailand', 'nameId': 'Thailand' },
    { 'code': 'TL', 'code3': 'TLS', 'nameEn': 'Timor-Leste', 'nameId': 'Timor Leste' },
    { 'code': 'TG', 'code3': 'TGO', 'nameEn': 'Togo', 'nameId': 'Togo' },
    { 'code': 'TO', 'code3': 'TON', 'nameEn': 'Tonga', 'nameId': 'Tonga' },
    { 'code': 'TT', 'code3': 'TTO', 'nameEn': 'Trinidad and Tobago', 'nameId': 'Trinidad dan Tobago' },
    { 'code': 'TN', 'code3': 'TUN', 'nameEn': 'Tunisia', 'nameId': 'Tunisia' },
    { 'code': 'TR', 'code3': 'TUR', 'nameEn': 'Turkey', 'nameId': 'Turki' },
    { 'code': 'TM', 'code3': 'TKM', 'nameEn': 'Turkmenistan', 'nameId': 'Turkmenistan' },
    { 'code': 'TV', 'code3': 'TUV', 'nameEn': 'Tuvalu', 'nameId': 'Tuvalu' },
    { 'code': 'UG', 'code3': 'UGA', 'nameEn': 'Uganda', 'nameId': 'Uganda' },
    { 'code': 'UA', 'code3': 'UKR', 'nameEn': 'Ukraine', 'nameId': 'Ukraina' },
    { 'code': 'AE', 'code3': 'ARE', 'nameEn': 'United Arab Emirates', 'nameId': 'Uni Emirat Arab' },
    { 'code': 'GB', 'code3': 'GBR', 'nameEn': 'United Kingdom', 'nameId': 'Inggris Raya' },
    { 'code': 'US', 'code3': 'USA', 'nameEn': 'United States', 'nameId': 'Amerika Serikat' },
    { 'code': 'UY', 'code3': 'URY', 'nameEn': 'Uruguay', 'nameId': 'Uruguay' },
    { 'code': 'UZ', 'code3': 'UZB', 'nameEn': 'Uzbekistan', 'nameId': 'Uzbekistan' },
    { 'code': 'VU', 'code3': 'VUT', 'nameEn': 'Vanuatu', 'nameId': 'Vanuatu' },
    { 'code': 'VA', 'code3': 'VAT', 'nameEn': 'Vatican City', 'nameId': 'Vatikan' },
    { 'code': 'VE', 'code3': 'VEN', 'nameEn': 'Venezuela', 'nameId': 'Venezuela' },
    { 'code': 'VN', 'code3': 'VNM', 'nameEn': 'Vietnam', 'nameId': 'Vietnam' },
    { 'code': 'YE', 'code3': 'YEM', 'nameEn': 'Yemen', 'nameId': 'Yaman' },
    { 'code': 'ZM', 'code3': 'ZMB', 'nameEn': 'Zambia', 'nameId': 'Zambia' },
    { 'code': 'ZW', 'code3': 'ZWE', 'nameEn': 'Zimbabwe', 'nameId': 'Zimbabwe' },
]

NORMALIZED_MAP = {}
DISPLAY_MAP = {} 

for c in COUNTRY_DATA:
    iso2 = c['code']
    display_name = c['nameEn']
    
    keys = [
        c['code'].lower(),
        c['code3'].lower(),
        c['nameEn'].lower(),
        c['nameId'].lower()
    ]
    
    DISPLAY_MAP[iso2] = display_name
    
    for k in keys:
        NORMALIZED_MAP[k] = iso2



HIGH_RISK_JURISDICTIONS = {
    'IR', # Iran
    'SY', # Syria
    'PK', # Pakistan
    'JO', # Jordan
    'TR', # Turkey
    'AE', # UAE
    'ZA', # South Africa
    'NG', # Nigeria
    'YE', # Yemen
    'KP', # North Korea
    'RU', # Russia
    'AF', # Afghanistan
    'IQ', # Iraq
    'CU', # Cuba
    'SD', # Sudan
    'SS'  # South Sudan
}

# Regional Blocs (ISO-2)
REGIONAL_BLOCS = {
    "ASEAN": [
        'ID', 'MY', 'SG', 'TH', 'VN', 'PH', 'BN', 'KH', 'LA', 'MM', 'TL'
    ],
    "EU": [
        'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 
        'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 
        'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'
    ]
}

# --- 4. FUNGSI UTAMA ---

def get_iso2_code(input_str: str) -> str | None:
    """Konversi input apapun (nama/kode) ke ISO-2 code."""
    if not isinstance(input_str, str):
        return None
    clean_input = input_str.lower().strip()
    return NORMALIZED_MAP.get(clean_input)

def get_country_display(input_str: str) -> str:
    """Mengambil nama display cantik dari input apapun."""
    iso2 = get_iso2_code(input_str)
    if iso2:
        return DISPLAY_MAP.get(iso2, iso2)
    return input_str or "-"

def get_country_bloc(input_str: str) -> str | None:
    """Cek blok regional berdasarkan input."""
    iso2 = get_iso2_code(input_str)
    if not iso2:
        return None
        
    for bloc_name, members in REGIONAL_BLOCS.items():
        if iso2 in members:
            return bloc_name
    return None

def generate_geographic_insights(customer: Dict[str, Any], sanction: Dict[str, Any]) -> List[str]:
    """
    Menghasilkan insight geografis dengan pencocokan pintar (Bilingual & Multi-format).
    """
    insights = []

    # Ambil input mentah
    raw_c_cit = customer.get("Citizenship")
    raw_c_res = customer.get("Country_of_Residence")
    raw_c_pob = customer.get("Place_of_Birth")
    raw_s_cit = sanction.get("Citizenship")

    # Konversi ke ISO-2
    iso_c_cit = get_iso2_code(raw_c_cit)
    iso_c_res = get_iso2_code(raw_c_res)
    iso_c_pob = get_iso2_code(raw_c_pob)

    # Display Names (untuk pesan error yg enak dibaca)
    disp_c_cit = get_country_display(raw_c_cit)
    disp_c_res = get_country_display(raw_c_res)
    disp_s_cit = get_country_display(raw_s_cit)

    # 1. High Risk Check (Citizenship)
    if iso_c_cit in HIGH_RISK_JURISDICTIONS:
        insights.append(
            f"⚠️ *Yurisdiksi Berisiko Tinggi:* Kewarganegaraan nasabah ({disp_c_cit}) "
            f"masuk dalam daftar pemantauan risiko tinggi."
        )

    
    if iso_c_res in HIGH_RISK_JURISDICTIONS:
        insights.append(
            f"⚠️ *Yurisdiksi Berisiko Tinggi:* Lokasi tempat tinggal/transaksi ({disp_c_res}) "
            f"masuk dalam daftar pemantauan risiko tinggi."
        )

    
    c_bloc = get_country_bloc(raw_c_cit)
    s_bloc = get_country_bloc(raw_s_cit)
    
    if c_bloc and s_bloc and c_bloc == s_bloc:
        insights.append(
            f"ℹ️ *Kedekatan Regional:* Nasabah ({disp_c_cit}) dan entitas sanksi "
            f"({disp_s_cit}) berasal dari kawasan regional yang sama ({c_bloc})."
        )

    
    
    risk_hits = set()
    for iso in [iso_c_cit, iso_c_res, iso_c_pob]:
        if iso and iso in HIGH_RISK_JURISDICTIONS:
            risk_hits.add(DISPLAY_MAP.get(iso))
            
    if len(risk_hits) >= 2:
        countries_str = ", ".join(risk_hits)
        insights.append(
            f"🚩 *Anomali Geografis:* Terdeteksi eksposur ganda ke yurisdiksi berisiko tinggi "
            f"({countries_str})."
        )

    return insights