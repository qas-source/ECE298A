`default_nettype none

module tt_um_programmable_counter (
    input  wire [7:0] ui_in,    // Dedicated inputs: 8-bit value to load
    output wire [7:0] uo_out,   // Dedicated outputs: 8-bit counter value
    input  wire [7:0] uio_in,   // IOs: Input path (uio_in[0] used as load signal)
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // High when the design is enabled
    input  wire       clk,      // Clock
    input  wire       rst_n     // Active-low reset
);

    // Tie off unused bidirectional pins as inputs to avoid synthesis warnings
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0; 

    // Internal 8-bit register for the counter
    reg [7:0] count;

    // Define the load signal for clarity
    wire load = uio_in[0];

    // Define an output enable signal (e.g., using uio_in[1])
    wire oe = uio_in[1];

    // Tri-state output logic
    assign uo_out = oe ? count : 8'bz;

    // Add negedge rst_n to the sensitivity list for asynchronous reset
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 8'b0;
        end else if (ena) begin
            if (load) begin
                count <= ui_in;
            end else begin
                count <= count + 1'b1;
            end
        end
    end

endmodule