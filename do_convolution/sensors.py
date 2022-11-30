import numpy as np
import pandas as pd

__all__ = ['sentinel2', 'superdove']


def sentinel2(bands, band_muls, s2_band_9_flag):
    '''Function that convolves input spectral values bands to Sentinel-2 bands
    '''

    # Bands central wavelengths details found at:
    # https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/resolutions/spatial

    # Sentinel-2 spectral response functions found at:
    # https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/document-library/-/asset_publisher/Wk0TKajiISaR/content/sentinel-2a-spectral-responses
    # or: https://sentinels.copernicus.eu/documents/247904/685211/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.1.xlsx

    # Band 10 was not inlcuded as not common to Level-1C and Level-2A Sentinel2
    # sensors. If wanting to add it, please add the line below:
    # Band_10 = (np.trapz((conv_process.iloc[987:1063, 10]), axis = 0)) \
    #         / (np.trapz((bands.iloc[987:1063, 10]), axis = 0))
    # and add this to the band name: "Band10_1375" and add Band10 to the list

    # Band 9 is not inlcuded as default due to it being the reflectance of
    # water vapour, which is generally rarely used. It is just necessary to
    # turn the flag to True to also get Band 9 convolved reflectance

    convolved_dfs = []
    for col_name, band_df in band_muls.items():
        Band1 = (np.trapz((band_df.iloc[62:107, 0]), axis=0))  \
            / (np.trapz((bands.iloc[62:107, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[89:184, 1]), axis=0))  \
            / (np.trapz((bands.iloc[89:184, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[188:233, 2]), axis=0)) \
            / (np.trapz((bands.iloc[188:233, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[296:344, 3]), axis=0)) \
            / (np.trapz((bands.iloc[296:344, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[345:364, 4]), axis=0)) \
            / (np.trapz((bands.iloc[345:364, 4]), axis=0))
        Band6 = (np.trapz((band_df.iloc[381:399, 5]), axis=0)) \
            / (np.trapz((bands.iloc[381:399, 5]), axis=0))
        Band7 = (np.trapz((band_df.iloc[419:447, 6]), axis=0)) \
            / (np.trapz((bands.iloc[419:447, 6]), axis=0))
        Band8 = (np.trapz((band_df.iloc[423:557, 7]), axis=0)) \
            / (np.trapz((bands.iloc[423:557, 7]), axis=0))
        Band8a = (np.trapz((band_df.iloc[497:531, 8]), axis=0)) \
            / (np.trapz((bands.iloc[497:531, 8]), axis=0))
        Band11 = (np.trapz((band_df.iloc[1189:1332, 11]), axis=0)) \
            / (np.trapz((bands.iloc[1189:1332, 11]), axis=0))
        Band12 = (np.trapz((band_df.iloc[1728:1970, 12]), axis=0)) \
            / (np.trapz((bands.iloc[1728:1970, 12]), axis=0))

        if s2_band_9_flag:
            Band9 = (np.trapz((band_df.iloc[582:609, 9]), axis=0)) \
                    / (np.trapz((bands.iloc[582:609, 9]), axis=0))
            convolved = {'Band_name_and_centre_wavelength':
                         ["Band1_443", "Band2_490", "Band3_560",
                          "Band4_665", "Band5_705", "Band6_740",
                          "Band7_783", "Band8_842", "Band8A_865",
                          "Band9_940", "Band11_1610", "Band12_2190"],
                         col_name+'_conv':
                         [Band1, Band2, Band3, Band4, Band5, Band6, Band7,
                          Band8, Band8a, Band9, Band11, Band12]}
        else:
            convolved = {'Band_name_and_centre_wavelength':
                         ["Band1_443", "Band2_490", "Band3_560",
                          "Band4_665", "Band5_705", "Band6_740",
                          "Band7_783", "Band8_842", "Band8A_865",
                          "Band11_1610", "Band12_2190"],
                         col_name+'_conv':
                         [Band1, Band2, Band3, Band4, Band5, Band6, Band7,
                          Band8, Band8a, Band11, Band12]}

        convolved_product = pd.DataFrame(convolved)
        convolved_product.set_index('Band_name_and_centre_wavelength',
                                    inplace=True)
        convolved_dfs.append(convolved_product)

    return convolved_dfs


def superdove(bands, band_muls):
    '''Function that convolves input spectral values bands to Superdove bands
    '''

    # Bands central wavelengths details found at:
    # https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=1399&context=calcon

    # Superdove spectral response functions found at:
    # https://support.planet.com/hc/en-us/articles/360014290293-Do-you-provide-Relative-Spectral-Response-Curves-RSRs-for-your-satellites-
    # or: https://support.planet.com/hc/en-us/article_attachments/360017988517/Superdove.csv

    # NOTE: Ranges for the Blue band (Band 2) are very wide on the spectral
    #       response function file above.
    #       It was decided to use the central range that had no 0s in between

    convolved_dfs = []
    for col_name, band_df in band_muls.items():
        Band1 = (np.trapz((band_df.iloc[77:111, 0]), axis=0))  \
            / (np.trapz((bands.iloc[77:111, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[108:172, 1]), axis=0)) \
            / (np.trapz((bands.iloc[108:172, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[157:209, 2]), axis=0)) \
            / (np.trapz((bands.iloc[157:209, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[193:242, 3]), axis=0)) \
            / (np.trapz((bands.iloc[193:242, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[243:285, 4]), axis=0)) \
            / (np.trapz((bands.iloc[243:285, 4]), axis=0))
        Band6 = (np.trapz((band_df.iloc[291:339, 5]), axis=0)) \
            / (np.trapz((bands.iloc[291:339, 5]), axis=0))
        Band7 = (np.trapz((band_df.iloc[342:374, 6]), axis=0)) \
            / (np.trapz((bands.iloc[342:374, 6]), axis=0))
        Band8 = (np.trapz((band_df.iloc[490:545, 7]), axis=0)) \
            / (np.trapz((bands.iloc[490:545, 7]), axis=0))

        convolved = {'Band_name_and_centre_wavelength':
                     ["Band1_443", "Band2_490", "Band3_531", "Band4_565",
                      "Band5_610", "Band6_665", "Band7_705", "Band8_865"],
                     col_name+'_conv': [Band1, Band2, Band3, Band4, Band5,
                                        Band6, Band7, Band8]}

        convolved_product = pd.DataFrame(convolved)
        convolved_product.set_index('Band_name_and_centre_wavelength',
                                    inplace=True)
        convolved_dfs.append(convolved_product)

    return convolved_dfs
