

  <h3 align="center">Nearmap Ortho Download and Tracking</h3>

  <p align="center">
    Front End and Database Connection for Nearmap Ortho Downloads, Used alongside the Nearmap Python Library
    <br />
    <a href="https://github.com/nearmap/nearmap-python-api"><strong>Nearmap Python Library</strong></a>
    <br />
   
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


In the Engineering Space, High Resolution Locally Cashed Ortho Imagery is a necesity for many Design projects. This repo can be used to build out a front end downloader and connect to a pre-established tracking database through MongoDB

Here's why:
*WMS Limitations
*Better and more transparent Area Tracking
*Ease of use.

Use the `main.py` and `main_downloader.ui` along with the Nearmap Python Repo to get Started. Contact Customer Service to get Databse Connection Established. Will not work without Tracking Database Connection.

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [Pyhon](https://www.python.org/)
* [MongoDB](https://mongodb.com/)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Install the Python Nearmap Repository as well as two additonal libraries seen below.


### Prerequisites

Install the Python Nearmap Repository. 
<a href="https://github.com/nearmap/nearmap-python-api"><strong>Nearmap Python Library</strong></a>

### Installation

<div align="left">

  <h3 align="left">See Python Nearmap Repo Instructions, however, in addition you will need to install: 
</h3>

  <p align="left">
    DNSPython
    <br />
    <a href="https://anaconda.org/conda-forge/dnspython/"><strong>Nearmap Python Library</strong></a>
    <br />

  <p align="left">
    PyMongo
    <br />
    <a href="https://anaconda.org/conda-forge/pymongo"><strong>Nearmap Python Library</strong></a>
    <br />
   
  </p>
</div>

<!-- USAGE EXAMPLES -->
## Usage

<div align="left">

  <h4 align="left">See Python Nearmap Repo Instructions, however, in addition you will need to install: 
</h3>

  <p align="left">
    DNSPython
    <br />
    <a href="https://anaconda.org/conda-forge/dnspython/"><strong>Nearmap Python Library</strong></a>
    <br />

  <p align="left">
    PyMongo
    <br />
    <a href="https://anaconda.org/conda-forge/pymongo"><strong>Nearmap Python Library</strong></a>
    <br />
   
  </p>
</div>


Front End Example, Use this to make Data Query.

![alt text](
images/Front_End.png)

<p align="center">(<a href="#top">back to top</a>)</p>

After Data Query this is the Schema of the MongoDB Post. 

![alt text](
images/Schema.png)

Orignal AOI (Geojson)
![alt text](
images/CustomerAOI.png)

Returned Ortho Saved Locally, Merged and Reprojected. (resolution varies by request parameters)
![alt text](
images/Customer_Ortho.png)

Tracking can be done Via MongoDB Atlas application or By directly Querying the Database and reading Geojson.
![alt text](
images/Tracking_Dash.png)

Folium Geojson Draw
![alt text](
images/Folium_Dash.png)


<!-- ROADMAP -->
## Roadmap

- [ ] Add DSM as a Content Type
- [ ] Add Vector AI data as a Content Type


<p align="right">(<a href="#top">back to top</a>)</p>


