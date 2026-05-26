float mod(float x, float y)
{
    return x - y * floor(x/y);
}

// rainbow code from: https://www.shadertoy.com/view/lsfBWs

// level is [0,5], assumed to be a whole number
float3 rainbow(float level)
{
	/*
		Target colors
		=============
		
		L  x   color
		0  0.0 vec4(1.0, 0.0, 0.0, 1.0);
		1  0.2 vec4(1.0, 0.5, 0.0, 1.0);
		2  0.4 vec4(1.0, 1.0, 0.0, 1.0);
		3  0.6 vec4(0.0, 0.5, 0.0, 1.0);
		4  0.8 vec4(0.0, 0.0, 1.0, 1.0);
		5  1.0 vec4(0.5, 0.0, 0.5, 1.0);
	*/
	
	float r = float(level <= 2.0) + float(level > 4.0) * 0.5;
	float g = max(1.0 - abs(level - 2.0) * 0.5, 0.0);
	float b = (1.0 - (level - 4.0) * 0.5) * float(level >= 4.0);
	return float3(r, g, b);
}

float3 mix(float3 a, float3 b, float3 x)
{
    return a * (1 - x) + b * x;
}

float3 smoothRainbow (float x)
{
    float level1 = floor(x*6.0);
    float level2 = min(6.0, floor(x*6.0) + 1.0);
    
    float3 a = rainbow(level1);
    float3 b = rainbow(level2);
    
    return mix(a, b, x*6.0 - floor(x*6.0));
}

float4 mainImage(VertData v_in) : TARGET
{
    // 10 5x5 ascii characters, on the spectrum " .:-=+*#%@"
    int pix[250] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,
    0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,
    0,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,1,1,1,1,
    1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,1,0,1,0,0,
    0,1,1,0,1,0,0,1,0,0,1,0,0,1,1,1,0,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0};

    float2 iResolution = uv_size;
    float2 newRes = iResolution / 5.0;
    float2 uv = floor(v_in.uv * newRes) / newRes;
	float4 texColor = image.Sample(textureSampler, uv);
    float texGray = dot(texColor.rgb, float3(0.299, 0.587, 0.114));
    int index = int(texGray * 10.0);
    int ascii = pix[index*25 + int(mod((v_in.uv*iResolution).x,5.0))*5 + int(mod((v_in.uv*iResolution).y,5.0))];
    // int ascii = pix[index*25+5];
    // float c_ind = float(index*25 + int(mod((v_in.uv*iResolution).x,5.0))*5 + int(mod((v_in.uv*iResolution).y,5.0))) / 250.0;

    float3 rb = smoothRainbow(v_in.uv.x);
    float3 color = float3(float(ascii) * rb);

	return float4(color, 1.0);
    // return float4(float(ascii * 255), float(ascii * 255), float(ascii * 255), 1.0);
    // return float4(c_ind, c_ind, c_ind, 1.0);
}