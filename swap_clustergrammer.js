

var about_string = 'Zoom, scroll, and click buttons to interact with the clustergram. <a href="http://amp.pharm.mssm.edu/clustergrammer/help"> <i class="fa fa-question-circle" aria-hidden="true"></i> </a>';

function make_clust(inst_network) {

    d3.json('json/'+inst_network, function(network_data) {

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

      d3.select(window).on('resize',function() {
        resize_container(args);
        cgm.resize_viz();
      });

      d3.select(window).on()

      cgm = Clustergrammer(args);

      d3.select(".expand_button").remove()

      d3.select(cgm.params.root + ' .wait_message').remove();

      In(null, function() {} , 0); // This is really hacky but it works

  });

};

function resize_container(args){

  console.log("resizing")

  var screen_width = d3.select(".stage").style("width")
  var screen_height = d3.select(".stage").style("height");

  console.log(screen_width, screen_height)

  // var new_width = String(parseInt(screen_width.replace("px","")) - 5) + 'px';

  // console.log(new_width)

  d3.select(args.root)
    .style('width', screen_width)
    .style('height', screen_height);
};

function dendro_callback(dendro_data) {
  console.log("dendro_callback")
  console.log(dendro_data)
  console.log(dendro_data.__data__) // use this to get data from 
};

function filterClustergram(index, names) {

  // console.log(names)
  
  clearTimeout(timer);

  timer = setTimeout(function() {
      if (names.length == 0) {
        var selection = {}; // GET ALL ROWS
      } else {
        var selection = { 'row' : names.map(function(x) { return x.replace("_"," ")}) };
      };
      cgm.filter_viz_using_names(selection);
      // };

  }, 500);
};

function set_up_clustergram() {
  // Fly out scatter, fly in clustergram
  d3.select("#scatter").style("display","none");
  d3.select("#clustergram").style("display","block");

  // Change left menubar options
  d3.select("#colorby").attr("label", "Expand column");
  // d3.selectAll("iron-selected")
}

function set_up_scatter() {
  d3.select("#clustergram").style("display","none");
  d3.select("#scatter").style("display","block");
  d3.select("#colorby").attr("label", "Color by");
}

