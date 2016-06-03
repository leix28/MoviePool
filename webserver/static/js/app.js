var indexApp = angular.module('indexApp', []);
indexApp.controller('indexController', function indexController($scope, $http) {
    $http.get("/api/pop").success(function(data) {
        data.forEach(function(entry) {
            if (entry.title.length > 20) {
                entry.title = entry.title.substr(0, 20) + "...";
            }
        });
        $scope.results = data;
    });
});
indexApp.filter('reshape', function () {
    return function (input, sub_size) {
        var newArr = [];
        if(!input)return input;
        if(input.reshaped)
            return input.reshaped;
        for(var i=0; i<input.length; i+=sub_size)
            newArr.push(input.slice(i,i+sub_size));
        input.reshaped=newArr;
        return newArr;
    };
});


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
        if(input.reshaped)
            return input.reshaped;
        for(var i=0; i<input.length; i+=sub_size)
            newArr.push(input.slice(i,i+sub_size));
        input.reshaped=newArr;
        return newArr;
    };
});

var movieApp = angular.module('movieApp', []);

movieApp.controller('movieController', function movieController($scope, $http) {
    $scope.resources = {ready: false, list: []};
    $scope.imdbId = 'tt0068646';
    $scope.download = function(item){
        if(item.cached){
            $('#iframe_for_download').prop('src', '/api/download/'+item.download_id);
        }else if(item.progress >= 0){
            // TODO: 注册完成通知
        }else{
            $http.get('/api/cache/'+item.download_id).success(function(data){
                // TODO: 注册完成通知
            });
        }
    };
    $http.get("/api/movie/" + location.pathname.split('/')[2]).success(function(data){
      data.castslist = Array();
      data.casts.forEach(function(entry){
        data.castslist.push(entry.name);
      });
      data.directorslist = Array();
      data.directors.forEach(function(entry){
        data.directorslist.push(entry.name);
      });
      $scope.movie=data;
      console.log(data);
    })
    $http.get("/api/resources/"+$scope.imdbId).success(function(data){
        $scope.resources.list = data;
        $scope.resources.ready=true;
    });
});
