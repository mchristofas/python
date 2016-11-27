puts "Hello world"
puts "it's me again!"
puts 'what "kind" of sauce ?'

puts "i will now coun chicks:"
puts "hens #{25 + 30 / 6}"
puts "i will now count eggs:"
puts 3.0+2+1-5+4%2-1/4+6
puts 3+2<5-7
print "give me a number"
number = gets.chomp.to_i
bigger = number * 100
puts "a bigger number is #{bigger}."
print "give me anothe number:"
another = gets.chomp
number = another.to_i
smaller = number /100
puts "a smaller number is #{smaller}"
