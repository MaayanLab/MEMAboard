

var about_string = 'Zoom, scroll, and click buttons to interact with the clustergram. <a href="http://amp.pharm.mssm.edu/clustergrammer/help"> <i class="fa fa-question-circle" aria-hidden="true"></i> </a>';

function make_clust(inst_network) {
  // d3.select(".notification-dialog-2").style("display","block");
  // d3.select('#clustergram-container div').remove();
    // console.log("running make_clust")

    d3.json('json/'+inst_network, function(network_data) {

      // console.log(network_data)

      // define arguments object
      var args = {
        root: '#clustergram',
        'network_data': network_data,
        'about': about_string,
        'ini_expand': true, // this removes the sidebar
        // 'row_tip_callback':hzome.gene_info,
        // 'col_tip_callback':test_col_callback,
        // 'tile_tip_callback':test_tile_callback,
        // 'dendro_callback':dendro_callback, // USE THIS
        // 'matrix_update_callback':matrix_update_callback,
        'sidebar_width':150,
        'make_modals': false
        // 'ini_view':{'N_row_var':20}
      };

      resize_container(args);

      d3.select(window).on('resize',function(){
        // console.log("ON resize")
        // console.log("resizing clustergrammer")
        resize_container(args);
        cgm.resize_viz();
      });

      d3.select(window).on()

      cgm = Clustergrammer(args);

      d3.select(".expand_button").remove()
      // check_setup_enrichr(cgm);

      d3.select(cgm.params.root + ' .wait_message').remove();

      In(null, function() {} , 0); // This is really hacky but it works

  });

}

function resize_container(args){

  // var screen_width = 1000 + 'px';
  // var screen_width = parseInt(d3.select(".main").style("width"),10) - 300;
  var screen_width = d3.select(".stage").style("width");
  var screen_height = d3.select(".stage").style("height");

  // var screen_width = window.innerWidth - 100;
  // var screen_height = window.innerHeight - 100;

  d3.select(args.root)
    .style('width', screen_width)
    .style('height', screen_height);
}

function dendro_callback(dendro_data) {
  console.log("dendro_callback")
  console.log(dendro_data)
  console.log(dendro_data.__data__) // use this to get data from 
}

function filterClustergram(index) {

  console.log("setting wait true"); WAIT = true;
  setTimeout(function() { if (WAIT == true) { WAIT = false }; }, 3000);

  // setTimeout(function() {
  //   console.log("setting wait false"); WAIT = false;
  // }, 3000);

  setTimeout(function() {
      console.log("WAIT =",WAIT);
      if (index.length == 0 || typeof cgm == "undefined" || WAIT) {
      } else {
        console.log("FILTERING")
        var row_names = index.map(function(x) { return cgm.params.network_data.row_nodes_names[x] });
        cgm.filter_viz_using_names({'row': row_names});
      };
      // WAIT = false;
  }, 3000);

  // console.log("setting wait true"); WAIT = true;
  // WAIT = true;

  // WAIT = false;
  // if (WAIT) 
  // setTimeout(function() { console.log("setting wait false"); WAIT = false; }, 2000);


  // if (index.length == 0 || typeof cgm == "undefined" || WAIT) {
  // } else {
  //   console.log("filterClustergram")
  //   var row_names = index.map(function(x) { return cgm.params.network_data.row_nodes_names[x] });
  //   cgm.filter_viz_using_names({'row': row_names});
  // };
  // WAIT = true;
  // setTimeout(function() { WAIT = false; }, 2000);
};

