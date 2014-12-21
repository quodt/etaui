'use strict';

// Declare app level module which depends on filters, and services
angular.module('etaui', ['ngRoute'])
  .config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/current', {templateUrl: 'partials/current.html', controller: "currentController"});
    $routeProvider.when('/stats', {templateUrl: 'partials/stats.html', controller: "statsController"});
    $routeProvider.otherwise({redirectTo: '/current'});
  }])
  .controller("statsController", ['$scope', function($scope) {
  }])
  .controller("currentController", ['$scope', 'currentPoller', function($scope, currentPoller) {
    $scope.data = currentPoller.data;
    console.log($scope.data);
  }])
  .factory('currentPoller', ['$http', '$timeout', function($http, $timeout) {
      var data = { response: {}, calls: 0 };
      var poller = function() {
        $http.get('/api/v1/status').then(function(r) {
          data.response = r.data;
          data.calls++;
          $timeout(poller, 10000);
        });
      };
      poller();
      return {
        data: data
      };
  }]);
