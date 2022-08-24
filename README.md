<h1 align="center">리뷰 맛집</h1>
<p align="center"><img src="https://user-images.githubusercontent.com/75832544/186341537-be7f66ae-113e-47cc-8006-8539e74a69d7.png"></p>






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
    <li><a href="#project-structure">Project Structure</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

유저 작성 후기와 함께 구매한 상품 목록을 기반으로 연관 상품 및 카테고리 추천 서비스를 개발하였습니다.

![image](https://user-images.githubusercontent.com/75832544/186337409-a8a8f909-962a-40b3-b7c9-3d775a117f1c.png)

기존의 리뷰 및 신규 리뷰 데이터를 활용한 키워드 분석을 통해 연관 카테고리를 도출하고, 함께 구매한 상품을 기반으로 유저에게 직접 피드백을 받는 연관 상품 도출 방식을 구현하고 배포하였습니다.

<br>



### Built With

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
- ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
- ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

<br>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```



<br>

<!-- Project Structure -->
## Project Structure
```
├── core
│   └── utils.py
│   └── review_keyword.py
│
├── products
│   └── views.py
│   └── models.py
│
├── reviews
│   └── views.py
│   └── models.py
│
├── reviews
│   └── views.py
│   └── models.py
│
├── review_king
│   └── settings.py
│
├── manage.py
├── start.sh
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

- `products` : 연관 카테고리 및 연관 상품 추출 기능 구현
- `reviews` : 리뷰를 작성하고 S3로 해당 리뷰의 이미지 저장 및 리뷰 기반의 키워드 추출 기능 구현
- `users` : 기본적인 사용자 관련 기능 구현
- `core` : 리뷰에서 상품명을 추출하도록 함수 선언, jwt 및 로그인 데코레이터 
