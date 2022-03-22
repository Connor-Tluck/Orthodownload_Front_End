from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot
from examples.pipelines.production.imagery import get_tiles_production_mapping,reproject_tiles
from nearmap.auth import get_api_key
from nearmap import NEARMAP
import time
import sys
import os
from nearmap._download_lib import get_coords
import datetime
import json
from nearmap import __version__
from pymongo import MongoClient
import geopandas as gpd
from shapely.geometry import Polygon

try:
    from osgeo_utils import gdal_merge
except ImportError:
    from osgeo.utils import gdal_merge
try:
    from ujson import load, dump, dumps
except ModuleNotFoundError:
    from json import load, dump, dumps

# Connect to the Nearmap API for Python
nearmap = NEARMAP(get_api_key())  # Paste or type your API Key here as a string
def _exception_info():
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    return f'Exception type: {exception_type} | File name: {filename}, Line number: {line_number}'

def mongo_connector(mongo_user, mongo_pass,collection_name, geometry_data_request, error_code=None):

    #write the error code if necessary, default is None
    geometry_data_request['error_code'] = error_code
    try:
        database_connection = f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.ijjjl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = MongoClient(
            database_connection)
        db = client.client_data_requests  # all client data goes here to this database
        print('connected to Mongo DB for Client Data')
    except Exception as e:
        print(f'mongodb error| {e} | {_exception_info()}')
        print(f'Could not Connect to DB Mongo Database....Database URL attempted was: {database_connection}')

    try:
        result = db[str(collection_name)].insert_one(geometry_data_request)
        # Step 4: Print to the console the ObjectID of the new document
        print('Created Entry'.format(result.inserted_id))
        # Step 5: Tell us that you are done
        print('finished adding geometry to the Mongo DB Database!')
    except Exception as e:
        print(f'mongodb error| {e} | {_exception_info()}')
        print(f'Could not Connect to DB Mongo Database....Database URL attempted was: {database_connection}')


class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen,self).__init__()
        loadUi("main_downloader.ui",self)
        self.in_file = self.button_file_input.clicked.connect(self.openFileNameDialog)
        self.out_file = self.button_save_location.clicked.connect(self.saveFileDialog)
        self.button_run.clicked.connect(self.on_download)

    @pyqtSlot()
    def on_download(self):
        global database_storage_json
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()

        #confirm database connection FIRST before delivering Data
        try:
            mongo_user = self.mongo_user.text().strip()
            print(f'Mongo User is: {mongo_user}')

            mongo_pass = self.mongo_pass.text().strip()
            print(f'Mongo Pass is: {mongo_pass}')

            collection_name = self.collection_name.text().strip()
            print(f'Mongo Client Account Name is: {collection_name}')

            client_name = self.client_name.text().strip()
            print(f'Mongo Client Account Name is: {client_name}')

            print('Checking User Login Credentials Please Wait.....')

            # connect to the database once variables are set
            database_connection = f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.ijjjl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            client = MongoClient(
                database_connection)
            if client.server_info().get('ok') == 1.0:
                print('server login OK, Connected to Database')
            else:
                print('please confirm username and password')


            try:
                if self.project_number.text() == 'Your API Key Here':
                    print('You forgot your API key please try again!')
                elif start_date == end_date:
                    print('Your Dates cannot be the same please try again.')
                else:

                    # Connect to the Nearmap API for Python
                    # nearmap = NEARMAP(get_api_key())  # Paste or type your API Key here as a string
                    # print(f'Actual API key is: {nearmap.api_key}')

                    project_number = self.project_number.text()
                    print(f'project number is: {project_number}')

                    start_date = self.start_date.date().toPyDate()
                    print(f'Selected Start Date: {start_date}')

                    end_date = self.end_date.date().toPyDate()
                    print(f'Selected End Date: {end_date}')

                    selected_content = self.content_type.currentText()
                    print(f'Selected Content is: {selected_content}')

                    zoom = self.tile_size.value()
                    print(f'tile size is: {str(zoom)}')

                    processing_method = self.processing_method.currentText()
                    print(f'processing_method is: {processing_method}')

                    epsg_code = self.epsg_code.text()
                    print(f'epsg_code is: {epsg_code}')

                    tile_size = self.tile_size.text()
                    print(f'tile_size is: {tile_size}')

                    # zip_size = self.zip_size.text()
                    # print(f'zip_size is: {zip_size}')

                    zip_size = 16  # fixed zip size for performance improvments.

                    print(f'Selected Content path is: {input_file}')
                    print(f'Save Location is defined as: {save_file_path}')
                    print('Download_my_Data')

                    # here are the download functions
                    since = start_date
                    until = end_date
                    packs = None
                    mosaic = None
                    fields = None
                    include = None
                    exclude = None
                    tertiary = None
                    out_ai_format = "gpkg"  # Of Type: "json" or "gpkg"
                    out_ortho_format = "tif"
                    out_format = "tif"  # Member of "tif", "jpg", "jp2", "png", "cog"
                    in_feature = input_file
                    out_folder = save_file_path
                    out_manifest = True  # Output a manifest of data extracted

                    '''fixed values below'''
                    buffer_distance = 0  # 0.5, 1, 5, 10 .... Distance in meters to offset by
                    remove_holes = True
                    out_image_format = 'tif'  # 'zip', 'tif', 'jpg
                    compression = 'JPEG'  # [JPEG/LZW/PACKBITS/DEFLATE/CCITTRLE/CCITTFAX3/CCITTFAX4/LZMA/ZSTD/LERC/LERC_DEFLATE/LERC_ZSTD/WEBP/JXL/NONE]
                    jpeg_quality = 75  # Only used if using JPEG Compression range[1-100]..

                    if processing_method == 'None':
                        processing_method = None
                    else:
                        processing_method = processing_method  # "mask" "bounds" or None <-- Enables Masking or clipping of image to input polygon but takes much longer to process

                    input = in_feature
                    output_dir = out_folder

                    # add geometry information to the mongodb database.
                    currentDateTime = datetime.datetime.now()
                    coords = get_coords(in_file=in_feature)

                    # Loading or Opening the json file
                    with open(input_file) as file:
                        file_data = json.load(file)
                    coords = file_data.get('features')[0].get('geometry').get('coordinates')[0]

                    shapely_polygon = Polygon([tuple(l) for l in coords])
                    centroid = list(shapely_polygon.centroid.coords)[0]

                    wgs = 'epsg:4326'
                    gdf = gpd.GeoDataFrame(index=[0], crs=wgs, geometry=[shapely_polygon])
                    area = gdf['geometry'].to_crs({'proj': 'cea'}) \
                        .map(lambda p: p.area / 10 ** 6)
                    print(f'area is {area} sq km')

                    database_storage_json = {'error_code': None,  # assume no error to start
                                             'coverage_binary': 1,
                                             'code_version': str(__version__),
                                             'project_number': str(project_number),
                                             'user': str(mongo_user),
                                             'collection_name': str(collection_name),
                                             'client_name': str(client_name),
                                             'input_file': str(input_file),
                                             'output_file': str(save_file_path),
                                             'requested_time': currentDateTime,
                                             'start_date': datetime.datetime(start_date.year, start_date.month,
                                                                             start_date.day),
                                             'end_date': datetime.datetime(end_date.year, end_date.month,
                                                                           end_date.day),
                                             'projection': str(epsg_code),
                                             'selected_content': str(selected_content),
                                             'tile_size': int(tile_size),
                                             'zip_size': int(zip_size),
                                             'masking_method': str(processing_method),
                                             'time_to_deliver_data': None,
                                             'time_to_reproject_data': None,
                                             'total_processing_time': None,
                                             'request_area': float(area),
                                             'request_centroid': centroid,
                                             'geojson_data': file_data
                                             }

                    if selected_content == 'OrthoImagery':
                        print('--------------------')
                        print(in_feature)
                        print(out_folder)
                        print(out_format)
                        print(tertiary)
                        print(since)
                        print(until)
                        print(mosaic)
                        print(include)
                        print(exclude)

                        ###############################
                        # Survey Specific User Params
                        #############################

                        surveyid = None  # Optional for calling a specific survey...
                        tileResourceType = 'Vert'  # Currently only 'Vert' and 'North' are supported
                        tertiary = None
                        mosaic = None
                        include = None
                        exclude = None
                        rate_limit_mode = 'slow'

                        download_time_start = time.time()  # timing function for testing evaluations

                        try:
                            get_tiles_production_mapping.tile_downloader(nearmap, input, output_dir, out_manifest,
                                                                         zoom, buffer_distance, remove_holes,
                                                                         out_image_format,
                                                                         compression, jpeg_quality, zip_size,
                                                                         processing_method, surveyid,
                                                                         tileResourceType, tertiary, since,
                                                                         until, mosaic, include, exclude,
                                                                         rate_limit_mode)
                            download_time_end = time.time()
                            download_processing_time = (download_time_end - download_time_start) / 60
                            print(
                                f'Imagery was downloaded in {download_processing_time} minutes, this will be saved to DB.')
                        except Exception as e:
                            mongo_connector(mongo_user=mongo_user, mongo_pass=mongo_pass,
                                            collection_name=collection_name,
                                            geometry_data_request=database_storage_json, error_code=e)
                            print(f'error: | Ortho Download Failed  | {e} | {_exception_info()}')
                            print('Ortho Failed, Data written to Database')

                        try:
                            ###############
                            # Find the bottom of the directory and look for tiles
                            #############
                            starting_directory = output_dir
                            lowest_dirs = list()
                            for root, dirs, files in os.walk(starting_directory):
                                if not dirs:
                                    lowest_dirs.append(root)

                            for directory in lowest_dirs:
                                for root, dirs, files in os.walk(directory):
                                    if len(files) != 0:
                                        pass
                                    else:
                                        print(f'no files in directory: {directory}')
                                        database_storage_json[
                                            'coverage_binary'] = 0  # not full coverage set flag to 0.

                            input_dir = lowest_dirs[0]  # this is a list atm
                            output_dir = lowest_dirs[0] + '/output'

                            tile_manifest = None
                            epsg_code = str(epsg_code)
                            output_crs = epsg_code  # Example: NAD83 Florida East (ftUS) | Lookup your CRS at: http://www.spatialreference.org
                            start_reproject = time.time()
                            try:
                                reproject_tiles.reprojection(input_dir, output_dir, tile_manifest,
                                                             output_crs=output_crs)
                            except:
                                print('No imagery to merge, pass and add to database at the end with error code')

                            end_reproject = time.time()  # timing function for testing evaluations
                            reproject_processing_time = (end_reproject - start_reproject) / 60
                            print(
                                f'Imagery was Reprojected in {reproject_processing_time} minutes, this will be saved to DB.')
                        except Exception as e:
                            mongo_connector(mongo_user=mongo_user, mongo_pass=mongo_pass,
                                            collection_name=collection_name,
                                            geometry_data_request=database_storage_json, error_code=e)
                            print(f'error: | failed  | {e} | {_exception_info()}')
                            print('Reprojection Failed Error Written to Database')

                    total_processing_time = float(download_processing_time) + float(reproject_processing_time)
                    print(
                        f'Data Download Complete, Writing to Customer Database....Time to Process was:{total_processing_time} minutes')

                    # everything went well, try to write the time values for ortho and reproject.
                    database_storage_json['time_to_deliver_data'] = download_processing_time
                    database_storage_json['time_to_reproject_data'] = reproject_processing_time
                    database_storage_json['total_processing_time'] = total_processing_time

                    if database_storage_json['coverage_binary'] == 1:  # data was coveraged
                        mongo_connector(mongo_user=mongo_user, mongo_pass=mongo_pass,
                                        collection_name=collection_name,
                                        geometry_data_request=database_storage_json)

                    else:
                        mongo_connector(mongo_user=mongo_user, mongo_pass=mongo_pass,
                                        collection_name=collection_name,
                                        geometry_data_request=database_storage_json,
                                        error_code='Coverage Gaps Found, No Data Returned.')

            except Exception as e:
                mongo_connector(mongo_user=mongo_user, mongo_pass=mongo_pass, collection_name=collection_name,
                                geometry_data_request=database_storage_json, error_code=e)
                print(f'error: | Mongo_connection_failed  | {e} | {_exception_info()} No Data written to Database')



        except Exception as e:
            print('Missing user inputs please fill out username, password, collection name and client name.')
            print(f'error: | Mongo_connection_failed  | {e} | {_exception_info()} No Data written to Database')



    '''class features below here for button access'''
    def openFileNameDialog(self):
        global input_file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        in_feature = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)

        if in_feature:
            print(in_feature[0])
            input_file = in_feature[0]

    def saveFileDialog(self):
        global save_file_path
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)

        if file_path:
            print(file_path[0])
            save_file_path = file_path[0]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(1100)
    widget.setFixedWidth(1300)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting....")
