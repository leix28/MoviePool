var searchApp = angular.module('searchApp', []);
searchApp.controller('searchController', function searchController($scope, $http) {
    $http.get("/api/search" + location.search).success(function(data) {
        data.forEach(function(entry) {
            if (entry.title.length > 20) {
                entry.title = entry.title.substr(0, 20) + "...";
            }
        });
        $scope.results = data;
    });
});
searchApp.filter('reshape', function () {
    return function (input, sub_size) {
        var newArr = [];
        if(!input)return input;
        for(var i=0; i<input.length; i+=sub_size)
            newArr.push(input.slice(i,i+sub_size));
        return newArr;
    };
});

var movieApp = angular.module('movieApp', []);

movieApp.controller('movieController', function movieController($scope, $http) {
  $http.get("/api/movie/" + location.pathname.split('/')[2]);
});
