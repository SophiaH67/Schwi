package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Println("Usage: pow <string_prefix> <hash_prefix>")
		os.Exit(1)
	}

	string_prefix := os.Args[1]
	hash_prefix := os.Args[2]

	difficulty := len(hash_prefix)
	
	i := 0
	for {
		i++
		hash := md5.Sum([]byte(string_prefix + strconv.Itoa(i)))
		if hex.EncodeToString(hash[:])[:difficulty] == hash_prefix[:difficulty] {
			fmt.Printf("\n%s %x\n",string_prefix + strconv.Itoa(i), hash)
			break
		}
		// every 10 million iterations, print a . to indicate progress
		if i % 10_000_000 == 0 {
			fmt.Print(".")
		}
	}
}