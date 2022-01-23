// ImageJ macro to construct a circle given three points.

macro "Make Circle" {
    getSelectionCoordinates(x, y);
    if (x.length != 3)
        exit("ERROR: Three points required");

    print("x: [" + x[0] + ", " + x[1] + ", " + x[2] + "]");
    print("y: [" + y[0] + ", " + y[1] + ", " + y[2] + "]");

    r1 = x[0]*x[0] + y[0]*y[0];
    r2 = x[1]*x[1] + y[1]*y[1];
    r3= x[2]*x[2] + y[2]*y[2];

    a = x[0]*(y[1]-y[2]) - y[0]*(x[1]-x[2]) + x[1]*y[2] - x[2]*y[1];
    b = r1*(y[2]-y[1]) + r2*(y[0]-y[2]) + r3*(y[1]-y[0]);
    c = r1*(x[1]-x[2]) + r2*(x[2]-x[0]) + r3*(x[0]-x[1]);
    d = r1*(x[2]*y[1]-x[1]*y[2]) + r2*(x[0]*y[2]-x[2]*y[0]) + r3*(x[1]*y[0] - x[0]*y[1]);

    if (abs(a) < 1e-6)
       exit("ERROR: Points are collinear");

    x = -b/(2*a);
    y = -c/(2*a);
    r = sqrt((b*b+c*c - 4*a*d)/(4*a*a));

    print("center: [" + x + ", " + y + "]");
    print("diameter: " + 2*r);

    run("Add Selection...", "fill=#ffff00ff");
    makeOval(x - r, y - r, 2*r, 2*r);
}

// macro to measure the average radius and diameter of a circle or ellipse.

macro "Measure Circle" {
    if (Roi.getType != "oval")
        exit("ERROR: Oval selection required");

    Roi.getBounds(x, y, width, height);
    r1 = width / 2; r2 = height / 2;
    x = x + r1; y = y + r2;
    d = (r1 + r2); r = d/2;
    print("center: [" + x + ", " + y + "]");
    print("r1: " + r1 + " r2: " + r2);
    print("radius: " + r);
    print("diameter: " + d);

	table = "Circle Measurements";
    if (Table.title != table) {
    	Table.create(table);
    	Table.showRowIndexes(true);
    }
    i = Table.size;

	Table.set("Image", i, getTitle());
	Table.set("x", i, x);
	Table.set("y", i, x);
	Table.set("r", i, r);
	Table.set("d", i, d);
    Table.update(table);
}