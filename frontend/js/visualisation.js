console.log('🎨 visualization.js loading...');

window.visualizeNetwork = function() {
    console.log('=== Creating Network Graph ===');
    
    try {
        // Validate data exists
        if (!currentWalletData || !currentWalletData.network) {
            console.error('❌ No network data available');
            return;
        }
        
        const container = document.getElementById('networkGraph');
        if (!container) {
            console.error('❌ Container not found');
            return;
        }
        
        container.innerHTML = '';
        
        const networkData = currentWalletData.network;
        const width = container.clientWidth || 1100;
        const height = 650;
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        
        console.log('📊 Graph dimensions:', width, 'x', height);
        console.log('📊 Data:', networkData.nodes.length, 'nodes,', networkData.edges.length, 'edges');
        
        // Verify D3.js is loaded
        if (typeof d3 === 'undefined') {
            console.error('❌ D3.js not loaded');
            container.innerHTML = '<div style="text-align:center;padding:100px;color:red;font-size:20px;">ERROR: D3.js library not loaded</div>';
            return;
        }
        
        // Create SVG canvas
        const svg = d3.select('#networkGraph')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Background
        svg.append('rect')
            .attr('width', width)
            .attr('height', height)
            .attr('fill', isDark ? '#0a0a0a' : '#ffffff');
        
        console.log('✅ SVG created');
        
        // Define arrow markers for directed edges
        svg.append('defs').append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 30)
            .attr('markerWidth', 8)
            .attr('markerHeight', 8)
            .attr('orient', 'auto')
            .append('path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', isDark ? '#888' : '#000');
        
        // Physics simulation for node positioning
        const simulation = d3.forceSimulation(networkData.nodes)
            .force('link', d3.forceLink(networkData.edges).id(d => d.id).distance(150))
            .force('charge', d3.forceManyBody().strength(-600))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(40));
        
        // Create transaction links (edges)
        const link = svg.append('g')
            .selectAll('line')
            .data(networkData.edges)
            .enter()
            .append('line')
            .attr('stroke', isDark ? '#555' : '#000000')
            .attr('stroke-width', 3)
            .attr('stroke-opacity', 0.6)
            .attr('marker-end', 'url(#arrowhead)');
        
        console.log('✅ Links created:', networkData.edges.length);
        
        // Create wallet nodes with color coding
        const node = svg.append('g')
            .selectAll('circle')
            .data(networkData.nodes)
            .enter()
            .append('circle')
            .attr('r', d => {
                if (d.type === 'target') return 25;      // Largest
                if (d.type === 'mixer') return 20;       // Medium
                return 15;                                // Small
            })
            .attr('fill', d => {
                if (d.type === 'target') return '#0000FF';    // Blue - Target wallet
                if (d.type === 'mixer') return '#FF0000';     // Red - Mixer service
                if (d.suspicious) return '#FFA500';           // Orange - Suspicious
                return '#00FF00';                             // Green - Safe
            })
            .attr('stroke', isDark ? '#fff' : '#000')
            .attr('stroke-width', 3)
            .style('cursor', 'pointer')
            .call(d3.drag()
                .on('start', (event, d) => {
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                })
                .on('drag', (event, d) => {
                    d.fx = event.x;
                    d.fy = event.y;
                })
                .on('end', (event, d) => {
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }));
        
        console.log('✅ Nodes created:', networkData.nodes.length);
        
        // Add wallet address labels
        const label = svg.append('g')
            .selectAll('text')
            .data(networkData.nodes)
            .enter()
            .append('text')
            .text(d => d.label)
            .attr('font-size', 12)
            .attr('font-weight', 'bold')
            .attr('fill', isDark ? '#fff' : '#000')
            .attr('text-anchor', 'middle')
            .attr('dy', -30)
            .style('pointer-events', 'none');
        
        // Hover tooltips
        node.append('title')
            .text(d => `Address: ${d.id}\nType: ${d.type}\nVolume: $${d.volume.toLocaleString()}\nSuspicious: ${d.suspicious ? 'Yes' : 'No'}`);
        
        // Animation: Update positions on each frame
        simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node
                .attr('cx', d => Math.max(40, Math.min(width - 40, d.x)))
                .attr('cy', d => Math.max(40, Math.min(height - 40, d.y)));
            
            label
                .attr('x', d => Math.max(40, Math.min(width - 40, d.x)))
                .attr('y', d => Math.max(40, Math.min(height - 40, d.y)));
        });
        
        console.log('✅ Network graph rendered successfully');
        
    } catch (error) {
        console.error('💥 Error in visualizeNetwork:', error);
        console.error('Stack:', error.stack);
    }
}

console.log('✅ visualization.js loaded successfully');
console.log('visualizeNetwork available:', typeof window.visualizeNetwork === 'function');
