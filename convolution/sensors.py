import numpy as np
import pandas as pd

__all__ = ['sentinel2', 'sentinel3', 'superdove', 'landsat5', 'landsat7', 'landsat8', 'landsat9']


def sentinel2(self):
    """Function that convolves input ground reflectance values to Sentinel2 bands"""

    # Sentinel-2 Bands central wavelengths details found at:
    # https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/resolutions/spatial

    # Sentinel-2 spectral response functions found at:
    # https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/document-library/-/asset_publisher/Wk0TKajiISaR/content/sentinel-2a-spectral-responses
    # or: https://sentinels.copernicus.eu/documents/247904/685211/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.1.xlsx

    for col_name, band_df in self._band_muls.items():
        Band1 = (np.trapz((band_df.iloc[62:107, 0]), axis=0))  \
            / (np.trapz((self.srf.iloc[62:107, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[89:184, 1]), axis=0))  \
            / (np.trapz((self.srf.iloc[89:184, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[188:233, 2]), axis=0)) \
            / (np.trapz((self.srf.iloc[188:233, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[296:344, 3]), axis=0)) \
            / (np.trapz((self.srf.iloc[296:344, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[345:364, 4]), axis=0)) \
            / (np.trapz((self.srf.iloc[345:364, 4]), axis=0))
        Band6 = (np.trapz((band_df.iloc[381:399, 5]), axis=0)) \
            / (np.trapz((self.srf.iloc[381:399, 5]), axis=0))
        Band7 = (np.trapz((band_df.iloc[419:447, 6]), axis=0)) \
            / (np.trapz((self.srf.iloc[419:447, 6]), axis=0))
        Band8 = (np.trapz((band_df.iloc[423:557, 7]), axis=0)) \
            / (np.trapz((self.srf.iloc[423:557, 7]), axis=0))
        Band8a = (np.trapz((band_df.iloc[497:531, 8]), axis=0)) \
            / (np.trapz((self.srf.iloc[497:531, 8]), axis=0))
        Band9 = (np.trapz((band_df.iloc[582:609, 9]), axis=0)) \
            / (np.trapz((self.srf.iloc[582:609, 9]), axis=0))       
        Band10 = (np.trapz((band_df.iloc[987:1063, 10]), axis=0)) \
            / (np.trapz((self.srf.iloc[987:1063, 10]), axis=0))
        Band11 = (np.trapz((band_df.iloc[1189:1332, 11]), axis=0)) \
            / (np.trapz((self.srf.iloc[1189:1332, 11]), axis=0))
        Band12 = (np.trapz((band_df.iloc[1728:1970, 12]), axis=0)) \
            / (np.trapz((self.srf.iloc[1728:1970, 12]), axis=0))

        convolved_col = pd.Series([Band1, Band2, Band3, Band4, Band5,
                                   Band6, Band7, Band8, Band8a, Band9,
                                   Band10, Band11, Band12], index=self.convolved_bands.index,
                                  name = col_name+'_conv')

        self.convolved_bands = pd.concat([self.convolved_bands, convolved_col], axis=1)

def sentinel3(self, srf, band_muls, convolved_bands):
    """Function that convolves input ground reflectance values to Sentinel3 bands"""

    # Bands central wavelengths details and Spectral response functions found at
    # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-3-olci/olci-instrument/spectral-characterisation-data

    for col_name, band_df in band_muls.items():
        Band1 = (np.trapz((band_df.iloc[37:62, 0]), axis=0)) \
            / (np.trapz((srf.iloc[37:62, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[52:72, 1]), axis=0)) \
            / (np.trapz((srf.iloc[52:72, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[83:103, 2]), axis=0)) \
            / (np.trapz((srf.iloc[83:103, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[131:150, 3]), axis=0)) \
            / (np.trapz((srf.iloc[131:150, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[151:170, 4]), axis=0)) \
            / (np.trapz((srf.iloc[151:170, 4]), axis=0))
        Band6 = (np.trapz((band_df.iloc[201:220, 5]), axis=0)) \
            / (np.trapz((srf.iloc[201:220, 5]), axis=0))
        Band7 = (np.trapz((band_df.iloc[261:280, 6]), axis=0)) \
            / (np.trapz((srf.iloc[261:280, 6]), axis=0))
        Band8 = (np.trapz((band_df.iloc[305:325, 7]), axis=0)) \
            / (np.trapz((srf.iloc[305:325, 7]), axis=0))
        Band9 = (np.trapz((band_df.iloc[315:333, 8]), axis=0)) \
            / (np.trapz((srf.iloc[315:333, 8]), axis=0))
        Band10 = (np.trapz((band_df.iloc[323:340, 9]), axis=0)) \
            / (np.trapz((srf.iloc[323:340, 9]), axis=0))
        Band11 = (np.trapz((band_df.iloc[349:369, 10]), axis=0)) \
            / (np.trapz((srf.iloc[349:369, 10]), axis=0))
        Band12 = (np.trapz((band_df.iloc[396:413, 11]), axis=0)) \
            / (np.trapz((srf.iloc[396:413, 11]), axis=0))
        Band13 = (np.trapz((band_df.iloc[406:418, 12]), axis=0)) \
            / (np.trapz((srf.iloc[406:418, 12]), axis=0))
        Band14 = (np.trapz((band_df.iloc[408:422, 13]), axis=0)) \
            / (np.trapz((srf.iloc[408:422, 13]), axis=0))
        Band15 = (np.trapz((band_df.iloc[412:424, 14]), axis=0)) \
            / (np.trapz((srf.iloc[412:424, 14]), axis=0))
        Band16 = (np.trapz((band_df.iloc[417:442, 15]), axis=0)) \
            / (np.trapz((srf.iloc[417:442, 15]), axis=0))
        Band17 = (np.trapz((band_df.iloc[501:530, 16]), axis=0)) \
            / (np.trapz((srf.iloc[501:530, 16]), axis=0))
        Band18 = (np.trapz((band_df.iloc[524:544, 17]), axis=0)) \
            / (np.trapz((srf.iloc[524:544, 17]), axis=0))
        Band19 = (np.trapz((band_df.iloc[539:559, 18]), axis=0)) \
            / (np.trapz((srf.iloc[539:559, 18]), axis=0))
        Band20 = (np.trapz((band_df.iloc[575:604, 19]), axis=0)) \
            / (np.trapz((srf.iloc[575:604, 19]), axis=0))
        Band21 = (np.trapz((band_df.iloc[645:694, 20]), axis=0)) \
            / (np.trapz((srf.iloc[645:694, 20]), axis=0))

        convolved_col = pd.Series([Band1, Band2, Band3, Band4, Band5, Band6,
                                   Band7, Band8, Band9, Band10, Band11, Band12,
                                   Band13, Band14, Band15, Band16, Band17, Band18,
                                   Band19, Band20, Band21], index=self.convolved_bands.index,
                                  name = col_name+'_conv')

        convolved_bands = pd.concat([convolved_bands, convolved_col], axis=1)
    return convolved_bands

def superdove(self):
    """Function that convolves input ground reflectance values to Superdove bands"""

    # Bands central wavelengths details found at:
    # https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=1399&context=calcon

    # Superdove spectral response functions found at:
    # https://support.planet.com/hc/en-us/articles/360014290293-Do-you-provide-Relative-Spectral-Response-Curves-RSRs-for-your-satellites-
    # or: https://support.planet.com/hc/en-us/article_attachments/360017988517/Superdove.csv

    # NOTE: Ranges for the Blue band (Band 2) are very wide on the spectral
    #       response function file above.
    #       Used the ranges with no 0s in between (guidance not provided by PlanetScope)

    for col_name, band_df in self._band_muls.items():
        Band1 = (np.trapz((band_df.iloc[77:111, 0]), axis=0))  \
            / (np.trapz((self.srf.iloc[77:111, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[108:172, 1]), axis=0)) \
            / (np.trapz((self.srf.iloc[108:172, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[157:209, 2]), axis=0)) \
            / (np.trapz((self.srf.iloc[157:209, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[193:242, 3]), axis=0)) \
            / (np.trapz((self.srf.iloc[193:242, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[243:285, 4]), axis=0)) \
            / (np.trapz((self.srf.iloc[243:285, 4]), axis=0))
        Band6 = (np.trapz((band_df.iloc[291:339, 5]), axis=0)) \
            / (np.trapz((self.srf.iloc[291:339, 5]), axis=0))
        Band7 = (np.trapz((band_df.iloc[342:374, 6]), axis=0)) \
            / (np.trapz((self.srf.iloc[342:374, 6]), axis=0))
        Band8 = (np.trapz((band_df.iloc[490:545, 7]), axis=0)) \
            / (np.trapz((self.srf.iloc[490:545, 7]), axis=0))

        convolved_col = pd.Series([Band1, Band2, Band3, Band4, Band5,
                                   Band6, Band7, Band8], index=self.convolved_bands.index,
                                  name = col_name+'_conv')

        self.convolved_bands = pd.concat([self.convolved_bands, convolved_col], axis=1)

def landsat5(self):
    """Function that convolves input ground reflectance values to Landsat5 bands"""

    # Landsat 5 spectral response functions found at:
    # https://landsat.usgs.gov/spectral-characteristics-viewer

    # Details of central wavelengths taken from:
    # 10.1016/j.rse.2009.01.007

    for col_name, band_df in self._band_muls.items():
        Band1 = (np.trapz((band_df.iloc[60:203, 0]), axis=0))  \
            / (np.trapz((self.srf.iloc[60:203, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[150:301, 1]), axis=0)) \
            / (np.trapz((self.srf.iloc[150:301, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[230:391, 2]), axis=0)) \
            / (np.trapz((self.srf.iloc[230:391, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[380:596, 3]), axis=0)) \
            / (np.trapz((self.srf.iloc[380:596, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[1164:1531, 4]), axis=0)) \
            / (np.trapz((self.srf.iloc[1164:1531, 4]), axis=0))
        Band7 = (np.trapz((band_df.iloc[1650:2051, 5]), axis=0)) \
            / (np.trapz((self.srf.iloc[1650:2051, 5]), axis=0))

        convolved_col = pd.Series([Band1, Band2, Band3, Band4, Band5, Band7],
                                  index=self.convolved_bands.index,
                                  name = col_name+'_conv')

        self.convolved_bands = pd.concat([self.convolved_bands, convolved_col], axis=1)

def landsat7(self):
    """Function that convolves input ground reflectance values to Landsat7 bands"""

    # Landsat 7 spectral response functions found at:
    # https://landsat.usgs.gov/spectral-characteristics-viewer

    # Details of central wavelengths taken from:
    # 10.1016/j.rse.2009.01.007

    for col_name, band_df in self._band_muls.items():
        Band1 = (np.trapz((band_df.iloc[60:174, 0]), axis=0))  \
            / (np.trapz((self.srf.iloc[60:174, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[150:301, 1]), axis=0)) \
            / (np.trapz((self.srf.iloc[150:301, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[230:391, 2]), axis=0)) \
            / (np.trapz((self.srf.iloc[230:391, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[380:596, 3]), axis=0)) \
            / (np.trapz((self.srf.iloc[380:596, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[1164:1531, 4]), axis=0)) \
            / (np.trapz((self.srf.iloc[1164:1531, 4]), axis=0))
        Band7 = (np.trapz((band_df.iloc[1650:2051, 5]), axis=0)) \
            / (np.trapz((self.srf.iloc[1650:2051, 5]), axis=0))
        Band8 = (np.trapz((band_df.iloc[150:591, 6]), axis=0)) \
            / (np.trapz((self.srf.iloc[150:591, 6]), axis=0))

        convolved_col = pd.Series([Band1, Band2, Band3, Band4, Band5, Band7,
                                   Band8],
                                  index=self.convolved_bands.index,
                                  name = col_name+'_conv')

        self.convolved_bands = pd.concat([self.convolved_bands, convolved_col], axis=1)

def landsat8(self, srf, band_muls, convolved_bands):
    """Function that convolves input ground reflectance values to Landsat8 bands"""

    # Landsat 8 spectral response functions found at:
    # https://landsat.usgs.gov/spectral-characteristics-viewer

    # Details of central wavelengths taken from:
    # https://doi.org/10.3390/rs61212275

    for col_name, band_df in band_muls.items():
        Band1 = (np.trapz((band_df.iloc[77:110, 0]), axis=0))  \
            / (np.trapz((srf.iloc[77:110, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[86:179, 1]), axis=0)) \
            / (np.trapz((srf.iloc[86:179, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[162:261, 2]), axis=0)) \
            / (np.trapz((srf.iloc[162:261, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[275:342, 3]), axis=0)) \
            / (np.trapz((srf.iloc[275:342, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[479:551, 4]), axis=0)) \
            / (np.trapz((srf.iloc[479:551, 4]), axis=0))
        Band6 = (np.trapz((band_df.iloc[1165:1348, 5]), axis=0)) \
            / (np.trapz((srf.iloc[1165:1348, 5]), axis=0))
        Band7 = (np.trapz((band_df.iloc[1687:2006, 6]), axis=0)) \
            / (np.trapz((srf.iloc[1687:2006, 6]), axis=0))
        Band8 = (np.trapz((band_df.iloc[138:343, 7]), axis=0)) \
            / (np.trapz((srf.iloc[138:343, 7]), axis=0))
        Band9 = (np.trapz((band_df.iloc[990:1060, 8]), axis=0)) \
            / (np.trapz((srf.iloc[990:1060, 8]), axis=0))

        convolved_col = pd.Series([Band1, Band2, Band3, Band4, Band5,
                                   Band6, Band7, Band8, Band9],
                                  index=self.convolved_bands.index,
                                  name = col_name+'_conv')

        convolved_bands = pd.concat([convolved_bands, convolved_col], axis=1)
    return convolved_bands

def landsat9(self, srf, band_muls, convolved_bands):
    """Function that convolves input ground reflectance values to Landsat9 bands"""

    # Landsat 9 spectral response functions found at:
    # https://landsat.usgs.gov/spectral-characteristics-viewer

    # Details of central wavelengths taken from:
    # https://doi.org/10.1117/12.2529776

    for col_name, band_df in band_muls.items():
        Band1 = (np.trapz((band_df.iloc[77:110, 0]), axis=0))  \
            / (np.trapz((srf.iloc[77:110, 0]), axis=0))
        Band2 = (np.trapz((band_df.iloc[86:181, 1]), axis=0)) \
            / (np.trapz((srf.iloc[86:181, 1]), axis=0))
        Band3 = (np.trapz((band_df.iloc[162:261, 2]), axis=0)) \
            / (np.trapz((srf.iloc[162:261, 2]), axis=0))
        Band4 = (np.trapz((band_df.iloc[275:342, 3]), axis=0)) \
            / (np.trapz((srf.iloc[275:342, 3]), axis=0))
        Band5 = (np.trapz((band_df.iloc[479:551, 4]), axis=0)) \
            / (np.trapz((srf.iloc[479:551, 4]), axis=0))
        Band6 = (np.trapz((band_df.iloc[1165:1348, 5]), axis=0)) \
            / (np.trapz((srf.iloc[1165:1348, 5]), axis=0))
        Band7 = (np.trapz((band_df.iloc[1687:2006, 6]), axis=0)) \
            / (np.trapz((srf.iloc[1687:2006, 6]), axis=0))
        Band8 = (np.trapz((band_df.iloc[138:343, 7]), axis=0)) \
            / (np.trapz((srf.iloc[138:343, 7]), axis=0))
        Band9 = (np.trapz((band_df.iloc[990:1060, 8]), axis=0)) \
            / (np.trapz((srf.iloc[990:1060, 8]), axis=0))

        convolved_col = pd.Series([Band1, Band2, Band3, Band4, Band5,
                                   Band6, Band7, Band8, Band9],
                                  index=self.convolved_bands.index,
                                  name = col_name+'_conv')

        convolved_bands = pd.concat([convolved_bands, convolved_col], axis=1)
    return convolved_bands
