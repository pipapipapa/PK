using System;


class Program
{
    static void Main(string[] args)
    {
        double a = Double.NaN, b = Double.NaN, c = Double.NaN;

        if (args.Length == 3)
        {
            if (double.TryParse(args[0], out a) && double.TryParse(args[1], out b) && double.TryParse(args[2], out c))
            {
                Console.WriteLine($"Коэффициенты: a = {a}, b = {b}, c = {c}");
            }

            else{
                Console.WriteLine("Некорректные коэффициенты.");
            }
        }


        if (a is Double.NaN || b is Double.NaN || c is Double.NaN)
        {
            Console.WriteLine("Введите коэффициенты:");

            Console.WriteLine("a = ");
            while (!double.TryParse(Console.ReadLine(), out a))
            {
                Console.WriteLine("Некорректный ввод.");
            }

            Console.WriteLine("b = ");
            while (!double.TryParse(Console.ReadLine(), out b))
            { 
                Console.WriteLine("Некорректный ввод.");
            }

            Console.WriteLine("c = ");
            while (!double.TryParse(Console.ReadLine(), out c))
            {
                Console.WriteLine("Некорректный ввод.");
            }
        }


        double D = b * b - 4 * a * c;

        if (D > 0){

            double x2_1 = (-b + Math.Sqrt(D)) / (2 * a);
            double x2_2 = (-b - Math.Sqrt(D)) / (2 * a);

            if (x2_1 >= 0 && x2_2 >= 0){
                double x1 = Math.Sqrt(x2_1);
                double x2 = Math.Sqrt(x2_2);
                Console.WriteLine($"Уравнение имеет 4 действительных корня: x1 = {x1}, x2 = {-x1}, x3 = {x2}, x4 = {-x2}");
            }

            else if (x2_1 >= 0){
                double x = Math.Sqrt(x2_1);
                Console.WriteLine($"Уравнение имеет 2 действительных корня: x1 = {x}, x2 = {-x}");
            }

            else if (x2_2 >= 0){
                double x = Math.Sqrt(x2_2);
                Console.WriteLine($"Уравнение имеет 2 действительных корня: x1 = {x}, x2 = {-x}");
            }

            else{
                Console.WriteLine("Уравнение не имеет действительных корней.");
            }

        }

        else if (D == 0){

            double x2 = -b / (2 * a);

            if (x2 >= 0){
                double x = Math.Sqrt(x2);
                Console.WriteLine($"Уравнение имеет два действительных корня: x1 = {x}, x2 = {-x}");
            }

            else{
                Console.WriteLine("Уравнение не имеет действительных корней.");
            }

        }

        else{
           Console.WriteLine("Уравнение не имеет действительных корней.");
        }
    }
}
