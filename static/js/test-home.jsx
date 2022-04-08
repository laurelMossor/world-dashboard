"use strict";

function RenderNews() {
    const [news, showNews] = React.useState([]);

    React.useEffect(() => {
        fetch("/news-country-test")
            .then((response) => response.json())
            .then((result) => {
                showNews(result);
            });
    }, []);

    const newsList = [news];

    return <p>newsList</p>
}


ReactDOM.render(<RenderNews />, 
document.querySelector('#news-dashboard'));
