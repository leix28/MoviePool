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

var searchApp = angular.module('movieApp', []);

searchApp.controller('movieController', function movieController($scope, $http) {
  $http.get("/api/movie/" + location.pathname.split('/')[2]);
});
