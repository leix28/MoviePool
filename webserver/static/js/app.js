var searchApp = angular.module('searchApp', []);

searchApp.controller('searchController', function searchController($scope, $http, $location) {
    $http.get("/api/search" + location.search).success(function(data) {
        data.forEach(function(entry) {
            if (entry.title.length > 20) {
                entry.title = entry.title.substr(0, 20) + "...";
            }
        });
        $scope.results = data;
    });
   
});
