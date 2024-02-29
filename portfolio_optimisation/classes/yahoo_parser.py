import pickle
import requests
import os

import bs4 as bs
import yfinance as yf
import pandas as pd

from typing import List, Optional
from datetime import datetime, date


class SP500Parser:
    def __init__(self) -> None:
        """
        Initializes an instance of the SP500Parser class.
        """
        self.tickers: Optional[List[str]] = None
        self.data: Optional[pd.DataFrame] = None

    def get_sp500_tickers(self) -> Optional[List[str]]:
        """
        Returns the list of S&P 500 company tickers.

        Returns:
        List[str]: A list of S&P 500 company tickers.
        """
        if self.tickers:
            return self.tickers

        resp = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        soup = bs.BeautifulSoup(resp.text, "lxml")
        table = soup.find("table", {"class": "wikitable sortable"})
        self.tickers = [
            row.findAll("td")[0].text.replace("\n", "")
            for row in table.findAll("tr")[1:]
        ]
        self.tickers.sort()

        return self.tickers

    def save_sp500_tickers(self) -> None:
        """
        Retrieves the list of S&P 500 company tickers from Wiki and saves it to a pickle file.
        """
        if not self.tickers:
            self.get_sp500_tickers()

        data_dir = "../data"

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        pickle_path = os.path.join(data_dir, "sp500tickers.pickle")

        with open(pickle_path, "wb") as f:
            pickle.dump(self.tickers, f)

    def download_sp500_data(
        self, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Downloads historical data for S&P 500 companies within the specified date range with 1 day granularity.
        Args:
            start_date (datetime): The start date for data retrieval.
            end_date (datetime): The end date for data retrieval.
        Returns:
            pd.DataFrame: A DataFrame containing historical data for S&P 500 companies.
        """
        if not self.tickers:
            self.get_sp500_tickers()

        data = yf.download(self.tickers, start=start_date, end=end_date, interval="1d")

        df = (
            data.stack()
            .reset_index()
            .rename(index=str, columns={"level_1": "Symbol"})
            .sort_values(["Symbol", "Date"])
            .set_index("Date")
        )
        self.data = df
        return self.data
['title_embedding_0', 'title_embedding_1', 'title_embedding_2', 'title_embedding_3', 'title_embedding_4', 'title_embedding_5', 'title_embedding_6', 'title_embedding_7', 'title_embedding_8', 'title_embedding_9', 'title_embedding_10', 'title_embedding_11', 'title_embedding_12', 'title_embedding_13', 'title_embedding_14', 'title_embedding_15', 'title_embedding_16', 'title_embedding_17', 'title_embedding_18', 'title_embedding_19', 'title_embedding_20', 'title_embedding_21', 'title_embedding_22', 'title_embedding_23', 'title_embedding_24', 'title_embedding_25', 'title_embedding_26', 'title_embedding_27', 'title_embedding_28', 'title_embedding_29', 'title_embedding_30', 'title_embedding_31', 'title_embedding_32', 'title_embedding_33', 'title_embedding_34', 'title_embedding_35', 'title_embedding_36', 'title_embedding_37', 'title_embedding_38', 'title_embedding_39', 'title_embedding_40', 'title_embedding_41', 'title_embedding_42', 'title_embedding_43', 'title_embedding_44', 'title_embedding_45', 'title_embedding_46', 'title_embedding_47', 'title_embedding_48', 'title_embedding_49', 'title_embedding_50', 'title_embedding_51', 'title_embedding_52', 'title_embedding_53', 'title_embedding_54', 'title_embedding_55', 'title_embedding_56', 'title_embedding_57', 'title_embedding_58', 'title_embedding_59', 'title_embedding_60', 'title_embedding_61', 'title_embedding_62', 'title_embedding_63', 'title_embedding_64', 'title_embedding_65', 'title_embedding_66', 'title_embedding_67', 'title_embedding_68', 'title_embedding_69', 'title_embedding_70', 'title_embedding_71', 'title_embedding_72', 'title_embedding_73', 'title_embedding_74', 'title_embedding_75', 'title_embedding_76', 'title_embedding_77', 'title_embedding_78', 'title_embedding_79', 'title_embedding_80', 'title_embedding_81', 'title_embedding_82', 'title_embedding_83', 'title_embedding_84', 'title_embedding_85', 'title_embedding_86', 'title_embedding_87', 'title_embedding_88', 'title_embedding_89', 'title_embedding_90', 'title_embedding_91', 'title_embedding_92', 'title_embedding_93', 'title_embedding_94', 'title_embedding_95', 'title_embedding_96', 'title_embedding_97', 'title_embedding_98', 'title_embedding_99', 'title_embedding_100', 'title_embedding_101', 'title_embedding_102', 'title_embedding_103', 'title_embedding_104', 'title_embedding_105', 'title_embedding_106', 'title_embedding_107', 'title_embedding_108', 'title_embedding_109', 'title_embedding_110', 'title_embedding_111', 'title_embedding_112', 'title_embedding_113', 'title_embedding_114', 'title_embedding_115', 'title_embedding_116', 'title_embedding_117', 'title_embedding_118', 'title_embedding_119', 'title_embedding_120', 'title_embedding_121', 'title_embedding_122', 'title_embedding_123', 'title_embedding_124', 'title_embedding_125', 'title_embedding_126', 'title_embedding_127', 'title_embedding_128', 'title_embedding_129', 'title_embedding_130', 'title_embedding_131', 'title_embedding_132', 'title_embedding_133', 'title_embedding_134', 'title_embedding_135', 'title_embedding_136', 'title_embedding_137', 'title_embedding_138', 'title_embedding_139', 'title_embedding_140', 'title_embedding_141', 'title_embedding_142', 'title_embedding_143', 'title_embedding_144', 'title_embedding_145', 'title_embedding_146', 'title_embedding_147', 'title_embedding_148', 'title_embedding_149', 'title_embedding_150', 'title_embedding_151', 'title_embedding_152', 'title_embedding_153', 'title_embedding_154', 'title_embedding_155', 'title_embedding_156', 'title_embedding_157', 'title_embedding_158', 'title_embedding_159', 'title_embedding_160', 'title_embedding_161', 'title_embedding_162', 'title_embedding_163', 'title_embedding_164', 'title_embedding_165', 'title_embedding_166', 'title_embedding_167', 'title_embedding_168', 'title_embedding_169', 'title_embedding_170', 'title_embedding_171', 'title_embedding_172', 'title_embedding_173', 'title_embedding_174', 'title_embedding_175', 'title_embedding_176', 'title_embedding_177', 'title_embedding_178', 'title_embedding_179', 'title_embedding_180', 'title_embedding_181', 'title_embedding_182', 'title_embedding_183', 'title_embedding_184', 'title_embedding_185', 'title_embedding_186', 'title_embedding_187', 'title_embedding_188', 'title_embedding_189', 'title_embedding_190', 'title_embedding_191', 'title_embedding_192', 'title_embedding_193', 'title_embedding_194', 'title_embedding_195', 'title_embedding_196', 'title_embedding_197', 'title_embedding_198', 'title_embedding_199', 'title_embedding_200', 'title_embedding_201', 'title_embedding_202', 'title_embedding_203', 'title_embedding_204', 'title_embedding_205', 'title_embedding_206', 'title_embedding_207', 'title_embedding_208', 'title_embedding_209', 'title_embedding_210', 'title_embedding_211', 'title_embedding_212', 'title_embedding_213', 'title_embedding_214', 'title_embedding_215', 'title_embedding_216', 'title_embedding_217', 'title_embedding_218', 'title_embedding_219', 'title_embedding_220', 'title_embedding_221', 'title_embedding_222', 'title_embedding_223', 'title_embedding_224', 'title_embedding_225', 'title_embedding_226', 'title_embedding_227', 'title_embedding_228', 'title_embedding_229', 'title_embedding_230', 'title_embedding_231', 'title_embedding_232', 'title_embedding_233', 'title_embedding_234', 'title_embedding_235', 'title_embedding_236', 'title_embedding_237', 'title_embedding_238', 'title_embedding_239', 'title_embedding_240', 'title_embedding_241', 'title_embedding_242', 'title_embedding_243', 'title_embedding_244', 'title_embedding_245', 'title_embedding_246', 'title_embedding_247', 'title_embedding_248', 'title_embedding_249', 'title_embedding_250', 'title_embedding_251', 'title_embedding_252', 'title_embedding_253', 'title_embedding_254', 'title_embedding_255', 'title_embedding_256', 'title_embedding_257', 'title_embedding_258', 'title_embedding_259', 'title_embedding_260', 'title_embedding_261', 'title_embedding_262', 'title_embedding_263', 'title_embedding_264', 'title_embedding_265', 'title_embedding_266', 'title_embedding_267', 'title_embedding_268', 'title_embedding_269', 'title_embedding_270', 'title_embedding_271', 'title_embedding_272', 'title_embedding_273', 'title_embedding_274', 'title_embedding_275', 'title_embedding_276', 'title_embedding_277', 'title_embedding_278', 'title_embedding_279', 'title_embedding_280', 'title_embedding_281', 'title_embedding_282', 'title_embedding_283', 'title_embedding_284', 'title_embedding_285', 'title_embedding_286', 'title_embedding_287', 'title_embedding_288', 'title_embedding_289', 'title_embedding_290', 'title_embedding_291', 'title_embedding_292', 'title_embedding_293', 'title_embedding_294', 'title_embedding_295', 'title_embedding_296', 'title_embedding_297', 'title_embedding_298', 'title_embedding_299', 'title_embedding_300', 'title_embedding_301', 'title_embedding_302', 'title_embedding_303', 'title_embedding_304', 'title_embedding_305', 'title_embedding_306', 'title_embedding_307', 'title_embedding_308', 'title_embedding_309', 'title_embedding_310', 'title_embedding_311', 'title_embedding_312', 'title_embedding_313', 'title_embedding_314', 'title_embedding_315', 'title_embedding_316', 'title_embedding_317', 'title_embedding_318', 'title_embedding_319', 'title_embedding_320', 'title_embedding_321', 'title_embedding_322', 'title_embedding_323', 'title_embedding_324', 'title_embedding_325', 'title_embedding_326', 'title_embedding_327', 'title_embedding_328', 'title_embedding_329', 'title_embedding_330', 'title_embedding_331', 'title_embedding_332', 'title_embedding_333', 'title_embedding_334', 'title_embedding_335', 'title_embedding_336', 'title_embedding_337', 'title_embedding_338', 'title_embedding_339', 'title_embedding_340', 'title_embedding_341', 'title_embedding_342', 'title_embedding_343', 'title_embedding_344', 'title_embedding_345', 'title_embedding_346', 'title_embedding_347', 'title_embedding_348', 'title_embedding_349', 'title_embedding_350', 'title_embedding_351', 'title_embedding_352', 'title_embedding_353', 'title_embedding_354', 'title_embedding_355', 'title_embedding_356', 'title_embedding_357', 'title_embedding_358', 'title_embedding_359', 'title_embedding_360', 'title_embedding_361', 'title_embedding_362', 'title_embedding_363', 'title_embedding_364', 'title_embedding_365', 'title_embedding_366', 'title_embedding_367', 'title_embedding_368', 'title_embedding_369', 'title_embedding_370', 'title_embedding_371', 'title_embedding_372', 'title_embedding_373', 'title_embedding_374', 'title_embedding_375', 'title_embedding_376', 'title_embedding_377', 'title_embedding_378', 'title_embedding_379', 'title_embedding_380', 'title_embedding_381', 'title_embedding_382', 'title_embedding_383', 'index', 'date', 'symbol', 'adj close', 'close', 'high', 'low', 'open', 'volume', 'lag_1', 'lag_2', 'lag_3', 'weekly_return', '5_day_ma', '20_day_ma', '5_day_volatility', 'momentum', 'macd', 'macd_signal', 'macd_histogram', 'week_of_year', 'month', 'body_preprocessed']
    def save_data_to_csv(self, file_name: str) -> None:
        """
        Saves the DataFrame to a CSV file.

        Args:
        file_name (str): The name of the CSV file.
        """
        if self.data is not None:
            self.data.to_csv(file_name)

    @staticmethod
    def download_custom_data(
        custom_tickers: List[str], start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Downloads historical data for custom companies within the specified date range with 1 day granularity.
        Args:
            custom_tickers (List[str]): List of specific tickers to parse.
            start_date (datetime): The start date for data retrieval.
            end_date (datetime): The end date for data retrieval.
        Returns:
            pd.DataFrame: A DataFrame containing historical data for S&P 500 companies.
        """

        data = yf.download(
            custom_tickers, start=start_date, end=end_date, interval="1d"
        )

        df = (
            data.stack()
            .reset_index()
            .rename(index=str, columns={"level_1": "Symbol"})
            .sort_values(["Symbol", "Date"])
            .set_index("Date")
        )
        return df
