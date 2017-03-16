
console.log("swappin")

// d3.selectAll("main").style("display","none")
// d3.selectAll("canvas").style("display","block")

// make_clust('mult_view.json');

var about_string = 'Zoom, scroll, and click buttons to interact with the clustergram. <a href="http://amp.pharm.mssm.edu/clustergrammer/help"> <i class="fa fa-question-circle" aria-hidden="true"></i> </a>';

function make_clust(inst_network) {

  // d3.select('#clustergram-container div').remove();
    // console.log("running make_clust")

    d3.json('json/'+inst_network, function(network_data) {

      // console.log(network_data)

      // define arguments object
      var args = {
        root: '#clustergram-container',
        'network_data': network_data,
        'about':about_string,
        'ini_expand': true, // this removes the sidebar
        // 'row_tip_callback':hzome.gene_info,
        // 'col_tip_callback':test_col_callback,
        // 'tile_tip_callback':test_tile_callback,
        // 'dendro_callback':dendro_callback,
        // 'matrix_update_callback':matrix_update_callback,
        'sidebar_width':150,
        // 'ini_view':{'N_row_var':20}
      };

      resize_container(args);

      cgm = Clustergrammer(args);

      d3.select(window).on('resize',function(){
        resize_container(args);
        cgm.resize_viz();
      });

      // cgm = Clustergrammer(args);

      d3.select(".expand_button").remove()
      // d3.select(".modal fade").remove()
      // d3.selectAll"
      // check_setup_enrichr(cgm);

      d3.select(cgm.params.root + ' .wait_message').remove();

  });

}

function resize_container(args){

  var screen_width = d3.select(".stage").style("width");
  var screen_height = d3.select(".stage").style("height");

  // var screen_width = window.innerWidth - 100;
  // var screen_height = window.innerHeight - 100;

  d3.select(args.root)
    .style('width', screen_width)
    .style('height', screen_height);
}
