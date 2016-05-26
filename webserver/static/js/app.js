var searchApp = angular.module('searchApp', []);

searchApp.controller('searchController', function searchController($scope, $http, $location) {
//      $scope.results = [
//    {
//      title: 'Nexus S',
//      snippet: 'Fast just got faster with Nexus S.'
//    }, {
//      title: 'Motorola XOOM™ with Wi-Fi',
//      snippet: 'The Next, Next Generation tablet.'
//    }, {
//      title: 'MOTOROLA XOOM™',
//      snippet: 'The Next, Next Generation tablet.'
//    }
//  ];
//    var tmp = $location.search();
//    console.log(tmp);
    $http({
        url: "/api/search",
        method: "GET",
        params: {"search":"abc"}//$location.search()
    }).success(function(data) {
        console.log(data);
        data.forEach(function(entry) {
            if (entry.title.length > 20) {
                entry.title = entry.title.substr(0, 20) + "...";
            }
        });
        $scope.results = data;
    });
   
});
